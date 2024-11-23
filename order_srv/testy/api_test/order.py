import json

import grpc

from order_srv.proto import order_pb2, order_pb2_grpc
from common.register.consul import ConsulRegister
from order_srv.settings import settings
from google.protobuf import empty_pb2


# 商品接口测试
class OrderTest:
    def __init__(self):
        # 连接grpc服务器
        rsp = ConsulRegister(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        order_srv = rsp.filter_service(service=settings.SERVICE_NAME)
        host, port = rsp.filter_host_port(order_srv)
        if not host:
            raise Exception("未找到grpc server")
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = order_pb2_grpc.OrderStub(channel)

    def getCartItemList(self):
        rsp: order_pb2.CartItemListResponse = self.stub.CartItemList(
            order_pb2.UserInfo(id=50)
        )
        for page in rsp.data:
            print("查询的数据", page.name, page.shopPrice)
    def CreateOrder(self):
        rsp = self.stub.CreateOrder(
            order_pb2.OrderRequest(userId=1,address="上海市",phone="18218218211",name="test",
                                   post="不错")
        )
        print(rsp)
    def CreateCartItem(self):
        rsp: order_pb2.ShopCartItemInfoResponse = self.stub.CreateCartItem(
            order_pb2.CartItemRequest(goodsId=422,userId=1,nums=5)
        )
        print(rsp)
    def OrderList(self):
        rsp = self.stub.OrderList(
            order_pb2.OrderFilterRequest(userId=1)
        )
        print(rsp)

if __name__ == '__main__':
    order = OrderTest()
    order.CreateOrder()
