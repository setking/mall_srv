import json

import grpc

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from common.register.consul import ConsulRegister
from inventory_srv.settings import settings
from google.protobuf import empty_pb2


# 库存接口测试
class InventoryTest:
    def __init__(self):
        # 连接grpc服务器
        rsp = ConsulRegister(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        srv = rsp.filter_service(service=settings.SERVICE_NAME)
        for k, v in srv.items():
            print(v["Address"], v["Port"])
            ip = v["Address"]
            port = v["Port"]
            break
        if not ip:
            raise Exception("未找到grpc server")
        channel = grpc.insecure_channel(f"{ip}:{port}")
        self.stub = inventory_pb2_grpc.InventoryStub(channel)

    def SetInv(self):
        rsp: empty_pb2.Empty() = self.stub.SetInv(
            inventory_pb2.GoodsInvInfo(goodsId=421, num=300)
        )
        print("设置成功", rsp)
    def GetInv(self):
        rsp: inventory_pb2.GoodsInvInfo = self.stub.GetInv(
            inventory_pb2.GoodsInvInfo(goodsId=6)
        )
        print("查询成功：", rsp)
    def SellInv(self):
        goods_list = [(421, 1), (422, 2),(423, 3)]
        request = inventory_pb2.SellInvInfo()
        for goodsId, num in goods_list:
            request.goodsInfo.append(inventory_pb2.GoodsInvInfo(goodsId=goodsId, num=num))
        rsp: empty_pb2.Empty() = self.stub.SellInv(request)
        print("扣减成功：", rsp)
    def RebackInv(self):
        goods_list = [(1, 3), (32, 4)]
        request = inventory_pb2.SellInvInfo()
        for goodsId, num in goods_list:
            request.goodsInfo.append(inventory_pb2.GoodsInvInfo(goodsId=goodsId, num=num))
        rsp: empty_pb2.Empty() = self.stub.RebackInv(request)
        print("归还成功：", rsp)

if __name__ == '__main__':
    import threading
    Inventory = InventoryTest()
    t1 = threading.Thread(target=Inventory.SetInv)
    t2 = threading.Thread(target=Inventory.SetInv)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
