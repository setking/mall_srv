from loguru import logger
from peewee import DoesNotExist

import grpc
import json

from order_srv.proto import order_pb2,order_pb2_grpc,goods_pb2,goods_pb2_grpc,inventory_pb2,inventory_pb2_grpc
from order_srv.model.models import ShoppingCart,OrderInfo,OrderGoods
from google.protobuf import empty_pb2
from common.register.consul import ConsulRegister
from order_srv.settings import settings
from rocketmq.client import Producer, Message, TransactionMQProducer, TransactionStatus, SendStatus, ConsumeStatus
import time
from datetime import datetime
import random
local_execute_dict = {}
def generate_order_sn(user_id):
    order_sn = f'{time.strftime("%Y%M%d%H%M%S")}{user_id}{random.randint(10,99)}'
    return order_sn
def delay_order_reback(msg):
    msg_body_str = msg.body.decode('utf-8')
    print(f"超时消息时间结算：{datetime.now()},接受内容：{msg_body_str}")
    msg_body = json.loads(msg_body_str)
    order_sn = msg_body["orderSn"]
    with settings.DB.atomic() as txn:
        try:
            order = OrderInfo.get(OrderInfo.order_sn == order_sn)
            if order.status != "TRADE_SUCCESS":
                order.status = "TRADE_CLOSED"
                order.save()
                #发送归还消息
                sync_msg = Message("order_reback")
                sync_msg.set_keys("order_srv")
                sync_msg.set_tags("delay_order")
                sync_msg.set_body(json.dumps({"orderSn": order_sn}))
                sync_producer = Producer("mall_send_order_srv")
                sync_producer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                sync_producer.start()
                ret = sync_producer.send_sync(sync_msg)
                if ret.status != SendStatus.OK:
                    raise Exception(f"Sync消息发送失败：{ret.status}")
                print(f"发送时间：{datetime.now()}")
                sync_producer.shutdown()
        except Exception as e:
            print(e)
            txn.rollback()
            return ConsumeStatus.RECONSUME_LATER
    return ConsumeStatus.CONSUME_SUCCESS


class OrderServicer(order_pb2_grpc.OrderServicer):
    #获取用户所有购物车信息
    @logger.catch
    def CartItemList(self, request: order_pb2.UserInfo, context):
        try:
            items = ShoppingCart.select().where(ShoppingCart.user == request.id)
            rsp = order_pb2.CartItemListResponse(total=items.count())
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()
        for item in items:
            item_rsp = order_pb2.ShopCartItemInfoResponse()
            item_rsp.id = item.id
            item_rsp.userId = item.user
            item_rsp.goodsId = item.goods
            item_rsp.nums = item.nums
            item_rsp.checked = item.checked
            rsp.data.append(item_rsp)
        return rsp
    #创建购物车商品
    @logger.catch
    def CreateCartItem(self, request: order_pb2.CartItemRequest, context):
        shoppingCart = ShoppingCart.select().where(ShoppingCart.goods == request.goodsId, ShoppingCart.user == request.userId)
        if shoppingCart:
            item = shoppingCart[0]
            item.nums += request.nums
        else:
            try:
                item = ShoppingCart()
                item.user = request.userId
                item.goods = request.goodsId
                item.nums = request.nums
            except DoesNotExist as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("商品创建失败")
                return order_pb2.ShopCartItemInfoResponse()
        item.save()
        return order_pb2.ShopCartItemInfoResponse(id=item.id)
    #更新购物车订单信息
    @logger.catch
    def UpdateCartItem(self, request: order_pb2.CartItemRequest, context):
        try:
            shoppingCart = ShoppingCart.get(ShoppingCart.user == request.userId,ShoppingCart.goods == request.goodsId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品查询失败")
            return empty_pb2.Empty()
        shoppingCart.nums = request.nums if request.nums else shoppingCart.nums
        shoppingCart.checked = request.checked
        shoppingCart.save()
        return empty_pb2.Empty()

    # 删除购物车商品
    @logger.catch
    def DeleteCartItem(self, request: order_pb2.CartItemRequest, context):
        try:
            order = ShoppingCart.get(ShoppingCart.user == request.userId, ShoppingCart.goods == request.goodsId)
            print(f"order:{order}")
            order.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return empty_pb2.Empty()

    @logger.catch
    def check_callback(self, msg):
        msg_body = json.loads(msg.body.decode('utf-8'))
        order_sn = msg_body["orderSn"]
        orders = OrderInfo.select().where(OrderInfo.order_sn == order_sn)
        if orders:
            return TransactionStatus.ROLLBACK
        else:
            return TransactionStatus.COMMIT

    @logger.catch
    def local_execute(self, msg, user_args):
        msg_body = json.loads(msg.body.decode('utf-8'))
        order_sn = msg_body["orderSn"]
        local_execute_dict[order_sn] = {}
        with settings.DB.atomic() as txn:
            """
            流程
            1. 价格从商品服务取
            2. 从库存服务扣减商品
            3. 从订单的商品信息表获取订单信息
            4. 从购物车获取选中商品
            5. 从购物车删除已购商品
            """
            # 购物车记录
            goods_ids = []
            goods_nums = {}
            order_amount = 0
            order_goods_list = []
            goods_sell_info = []
            for cart_item in ShoppingCart.select().where(ShoppingCart.user == msg_body["userId"], ShoppingCart.checked==True):
                goods_ids.append(cart_item.goods)
                goods_nums[cart_item.goods] = cart_item.nums
            if not goods_ids:
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.NOT_FOUND
                local_execute_dict[order_sn]["details"] = "没有结算商品"
                return TransactionStatus.ROLLBACK
            #商品信息
            register = ConsulRegister(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
            goods_srv = register.filter_service(service=settings.GOODS_SRV_NAME)
            inventory_srv = register.filter_service(service=settings.INVENTORY_SRV_NAME)
            inventory_srv_host, inventory_srv_port = register.filter_host_port(inventory_srv)
            goods_srv_host, goods_srv_port = register.filter_host_port(goods_srv)
            if not goods_srv_host:
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["details"] = "商品服务不可用"
                return TransactionStatus.ROLLBACK
            goods_channel = grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}")
            goods_stub = goods_pb2_grpc.GoodsStub(goods_channel)
            #批量获取商品信息
            try:
                goods_info_rsp = goods_stub.BatchGetGoods(goods_pb2.BatchGoodsIdInfo(id=goods_ids))
            except grpc.RpcError as e:
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["details"] = f"商品服务不可用:{str(e)}"
                return TransactionStatus.ROLLBACK
            for goods_info in goods_info_rsp.data:
                order_amount += goods_info.shopPrice*goods_nums[goods_info.id]
                order_goods = OrderGoods(goods=goods_info.id,goods_name=goods_info.name,
                                         goods_image=goods_info.goodsFrontImage,
                                         goods_price=goods_info.shopPrice,
                                         nums=goods_nums[goods_info.id])
                order_goods_list.append(order_goods)
                goods_sell_info.append(inventory_pb2.GoodsInvInfo(goodsId=goods_info.id,num=goods_nums[goods_info.id]))
            #扣减库存
            if not inventory_srv_host:
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["details"] = "库存服务不可用"
                return TransactionStatus.ROLLBACK
            inventory_channel = grpc.insecure_channel(f"{inventory_srv_host}:{inventory_srv_port}")
            inventory_stub = inventory_pb2_grpc.InventoryStub(inventory_channel)

            try:
                inventory_stub.SellInv(inventory_pb2.SellInvInfo(orderSn=order_sn,goodsInfo=goods_sell_info))
            except grpc.RpcError as e:
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["details"] = f"库存扣减失败:{str(e)}"
                err_code = e.code()
                if err_code == grpc.StatusCode.UNKNOWN or err_code == grpc.StatusCode.DEADLINE_EXCEEDED:
                    # 库存不足， 库存服务没有扣减库存，不需要发送归还库存消息
                    return TransactionStatus.COMMIT
                else:
                    return TransactionStatus.ROLLBACK
            try:
                # 创建订单
                order = OrderInfo()
                order.order_sn = order_sn
                order.order_amount = order_amount
                order.address = msg_body["address"]
                order.signer_name = msg_body["name"]
                order.signer_phone = msg_body["phone"]
                order.post = msg_body["post"]
                order.user = msg_body["userId"]
                order.save()
                # 批量插入商品订单列表
                for order_goods in order_goods_list:
                    order_goods.order = order.id
                OrderGoods.bulk_create(order_goods_list)
                # 删除记录
                ShoppingCart.delete().where(ShoppingCart.user == msg_body["userId"], ShoppingCart.checked == True).execute()
                local_execute_dict[order_sn] = {
                    "code": grpc.StatusCode.OK,
                    "details": "下单成功",
                    "order": {
                        "id": order.id,
                        "orderSn": order_sn,
                        "amount": order_amount,
                    }
                }
                #发送延时消息
                delay_msg = Message("delay_order_reback")
                delay_msg.set_keys("order_srv")
                delay_msg.set_tags("delay_order")
                delay_msg.set_body(json.dumps({"orderSn": order_sn}))
                delay_msg.set_delay_time_level(4)# 1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h
                delay_producer = Producer("mall_delay_order_srv")
                delay_producer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                delay_producer.start()
                ret = delay_producer.send_sync(delay_msg)
                if ret.status!= SendStatus.OK:
                    raise Exception(f"Delay消息发送失败：{ret.status}")
                print(f"发送时间：{datetime.now()}")
                delay_producer.shutdown()
            except Exception as e:
                txn.rollback()
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["details"] = f"订单创建失败:{str(e)}"
                return TransactionStatus.COMMIT
        return TransactionStatus.ROLLBACK
    #新建订单
    @logger.catch
    def CreateOrder(self, request: order_pb2.OrderRequest, context):
        producer = TransactionMQProducer("mall_order_srv", self.check_callback)
        producer.set_name_server_address(f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
        producer.start()
        msg = Message("order_reback")
        msg.set_keys("order_srv")
        msg.set_tags("order")

        order_sn = generate_order_sn(request.userId)
        msg_body = {
            "orderSn": order_sn,
            "userId": request.userId,
            "address": request.address,
            "name": request.name,
            "phone": request.phone,
            "post": request.post,
        }
        msg.set_body(json.dumps(msg_body))

        ret = producer.send_message_in_transaction(msg, self.local_execute, None)
        logger.info('发送消息状态: ' + str(ret.status) + ' 消息id: ' + ret.msg_id)
        if ret.status != SendStatus.OK:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("新建订单失败")
            return order_pb2.OrderInfoResponse()
        while True:
            if order_sn in local_execute_dict:
                context.set_code(local_execute_dict[order_sn]["code"])
                context.set_details(local_execute_dict[order_sn]["details"])
                producer.shutdown()
                if local_execute_dict[order_sn]["code"] == grpc.StatusCode.OK:
                    return order_pb2.OrderInfoResponse(id=local_execute_dict[order_sn]["order"]["id"], orderSn=local_execute_dict[order_sn]["order"]["orderSn"], amount=local_execute_dict[order_sn]["order"]["amount"])
                else:
                    return order_pb2.OrderInfoResponse()
            time.sleep(0.1)
    #订单列表
    @logger.catch
    def OrderList(self, request: order_pb2.OrderFilterRequest, context):
        items = OrderInfo.select()
        if request.userId:
            try:
                items = items.where(OrderInfo.user == request.userId)
            except DoesNotExist as e:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("记录不存在")
                return empty_pb2.Empty()
        rsp = order_pb2.OrderListResponse()
        rsp.total = items.count()
        # 分页 limit offset
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)
        items = items.limit(per_page_nums).offset(start)
        for item in items:
            item_rsp = order_pb2.OrderInfoResponse()
            item_rsp.id = item.id
            item_rsp.userId = item.user
            item_rsp.orderSn = item.order_sn
            item_rsp.payType = item.pay_type
            item_rsp.status = item.status
            item_rsp.amount = item.order_amount
            item_rsp.address = item.address
            item_rsp.name = item.signer_name
            item_rsp.phone = item.signer_phone
            rsp.data.append(item_rsp)
        return rsp

    @logger.catch
    def OrderDetail(self, request: order_pb2.OrderRequest, context):
        try:
            if request.userId:
                items = OrderInfo.get(OrderInfo.id == request.id, OrderInfo.user == request.userId)
            else:
                items = OrderInfo.get(OrderInfo.id == request.id)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return order_pb2.OrderInfoDetailResponse()
        rsp = order_pb2.OrderInfoDetailResponse()
        rsp.orderInfo.id = items.id
        rsp.orderInfo.userId = items.user
        rsp.orderInfo.orderSn = items.order_sn
        rsp.orderInfo.payType = items.pay_type
        rsp.orderInfo.status = items.status
        rsp.orderInfo.amount = items.order_amount
        rsp.orderInfo.post = items.post
        rsp.orderInfo.address = items.address
        rsp.orderInfo.name = items.signer_name
        rsp.orderInfo.phone = items.signer_name
        try:
            items_goods = OrderGoods.select().where(OrderGoods.order == items.id)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return order_pb2.OrderInfoDetailResponse()
        for items_good in items_goods:
            rsp_data = order_pb2.OrderItemResponse()
            rsp_data.goodsId = items_good.goods
            rsp_data.goodsName = items_good.goods_name
            rsp_data.goodsImage = items_good.goods_image
            rsp_data.goodsPrice = items_good.goods_price
            rsp_data.nums = items_good.nums
            rsp.data.append(rsp_data)
        return rsp
    #更新订单状态
    @logger.catch
    def UpdateOrder(self, request: order_pb2.OrderStatus, context):
        try:
            OrderInfo.update(status=request.status).where(OrderInfo.order_sn == request.orderSn).execute()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("订单记录不存在")
            return empty_pb2.Empty()
