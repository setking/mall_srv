import json
import time
from math import trunc


from loguru import logger
import grpc
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from peewee import DoesNotExist
from datetime import date
from inventory_srv.model.models import Inventory, InventoryHistory
from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.settings import settings
from google.protobuf import empty_pb2
from common.redis_lock import redis_lock
from rocketmq.client import PushConsumer, ConsumeStatus

def reback_inv(msg):
    msg_body_str = msg.body.decode("utf-8")
    print(f"收到消息：{msg_body_str}")
    msg_body = json.loads(msg_body_str)
    order_sn = msg_body["orderSn"]
    with settings.DB.atomic() as txn:
        # 库存回滚
        try:
            invs = InventoryHistory.get(InventoryHistory.order_sn == order_sn)
            inv_details = json.loads(invs.order_inv_detail)
            for item in inv_details:
                good_id = item["goodsId"]
                num = item["num"]
                Inventory.update(stocks=Inventory.stocks + num).where(Inventory.goods == good_id).execute()
            invs.status = 2
            invs.save()
            return ConsumeStatus.CONSUME_SUCCESS
        except DoesNotExist as e:
            return ConsumeStatus.CONSUME_SUCCESS
        except Exception as e:
            txn.rollback()
            return ConsumeStatus.RECONSUME_LATER


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):
    #库存设置
    @logger.catch
    def SetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        invs = Inventory.select().where(Inventory.goods == request.goodsId)
        force_insert = False
        if not invs:
            inv = Inventory()
            inv.goods = request.goodsId
            force_insert = True
        else:
            inv = invs[0]
        inv.stocks = request.num
        inv.save(force_insert=force_insert)
        return empty_pb2.Empty()
    #获取库存信息
    @logger.catch
    def GetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        try:
            inv = Inventory.get(Inventory.goods == request.goodsId)
            return inventory_pb2.GoodsInvInfo(goodsId=inv.goods,num=inv.stocks)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("没有库存记录")
            return inventory_pb2.GoodsInvInfo()
    #扣减库存
    @logger.catch
    def SellInv(self, request: inventory_pb2.SellInvInfo, context):
        inv_history = InventoryHistory(order_sn=request.orderSn)
        inv_detail = []
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                lock = redis_lock.Lock(settings.REDIS_CLIENT, f"lock:goods_{item.goodsId}", auto_renewal=True, expire=10)
                lock.acquire()
                try:
                    goods_inv = Inventory.get(Inventory.goods == item.goodsId)
                    print(f"商品{item.goodsId}售出{item.num}件")
                except DoesNotExist as e:
                    txn.rollback()  # 回滚事务
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("没有库存记录")
                    return empty_pb2.Empty()
                if goods_inv.stocks < item.num:
                    context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
                    context.set_details("库存不足")
                    txn.rollback()#回滚事务
                    return empty_pb2.Empty()
                else:
                    inv_detail.append({
                        "goodsId": item.goodsId,
                        "num": item.num
                    })
                    goods_inv.stocks -= item.num
                    goods_inv.save()
                lock.release()
            inv_history.order_inv_detail = json.dumps(inv_detail)
            inv_history.save()
            return empty_pb2.Empty()
    #库存归还
    @logger.catch
    def RebackInv(self, request: inventory_pb2.SellInvInfo, context):
        #1. 订单超时自动归还 2. 订单创建失败，需要归还之前的库存 3. 手动归还
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                lock = redis_lock.Lock(settings.REDIS_CLIENT, f"lock:goods_{item.goodsId}", auto_renewal=True,
                                       expire=10)
                lock.acquire()
                try:
                    goods_inv = Inventory.get(item.goodsId)
                except DoesNotExist as e:
                    txn.rollback()  # 回滚事务
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("没有库存记录")
                    return empty_pb2.Empty()
                goods_inv.stocks += item.num
                goods_inv.save()
            lock.release()
            return empty_pb2.Empty()
