import json

import grpc

from goods_srv.proto import goods_pb2, goods_pb2_grpc
from common.register.consul import ConsulRegister
from goods_srv.settings import settings
from google.protobuf import empty_pb2


# 商品接口测试
class GoodsTest:
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
        self.stub = goods_pb2_grpc.GoodsStub(channel)

    def Goods_list(self):
        rsp: goods_pb2.GoodsListResponse = self.stub.GoodsList(
            goods_pb2.GoodsFilterRequest(priceMin=50)
        )
        for page in rsp.data:
            print("查询的数据", page.name, page.shopPrice)

    def Batche_get_goods(self):
        ids = [421, 422, 423]
        rsp: goods_pb2.GoodsListResponse = self.stub.BatchGetGoods(
            goods_pb2.BatchGoodsIdInfo(id=ids)
        )
        for page in rsp.data:
            print("查询的数据", page.name, page.shopPrice)

    def delete_goods(self):
        id = 423
        rsp: empty_pb2.Empty() = self.stub.DeleteGoods(
            goods_pb2.DeleteGoodsInfo(id=id)
        )
        print("商品删除成功", rsp)

    def Get_goods_detail(self):
        id = 421
        rsp: goods_pb2.GoodsInfoResponse = self.stub.GetGoodsDetail(
            goods_pb2.GoodInfoRequest(id=id)
        )
        print("获取商品详情成功", rsp)

    def Create_goods(self):
        rsp: goods_pb2.CreateGoodsInfo = self.stub.CreateGoods(
            goods_pb2.CreateGoodsInfo(
                name="迁西板栗",
                categoryId=225638,
                brandId=618,
                goodsSn="12345678",
                marketPrice=1.00,
                shopPrice=1.00,
                goodsBrief="迁西板栗",
                shipFree=1,
                images=["https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/df392d01993cdab9de740fe17798bda1",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/0fbd1bdbec4f887bff071f86b450838a",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/03ae7aa0e2cf6aaedb6e1a3ac47ebdd8",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/f952a1776ccbe5458d35eb079a60d808",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/c9f8005aac083ffc035c07c32c908f80"],
                descImages=["https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/547087e0cbf3beb3c413d7a922fef275",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/5f587c274004a351cefc7362318bc92b",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/b2d6fafe36242f0badbc8135efd8f317",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/c5cd6d4da796436d39b22a0d89a4cc75",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/923dd72257832cacc2e6286052ce2b86",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/7b019206fa9c990a511f5cfba726816a",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/fbb0b858d1fb38ef373a207f27034756",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/faa29f57b1c1cff265630f36f983b3e7",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/02bfd8d19251f33a1215c87e205e7a52",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/3bda130cab8a7dac0bad9aa79ebd1d4b",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/3ad379cf4fb0962267a71dfca869ce0d",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/30661717224fb26af5e1ca93d17bb80f"],
                goodsFrontImage="https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/df392d01993cdab9de740fe17798bda1",
                isNew=1,
                isHot=0,
                onSale=1
            )
        )
        print("新建商品成功：", rsp)
    def Update_goods(self):
        rsp: goods_pb2.CreateGoodsInfo = self.stub.UpdateGoods(
            goods_pb2.CreateGoodsInfo(
                id=847,
                name="学区樱桃",
                categoryId=225638,
                brandId=618,
                goodsSn="567587876",
                marketPrice=1.00,
                shopPrice=1.00,
                goodsBrief="迁西板栗",
                shipFree=1,
                images=["https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/df392d01993cdab9de740fe17798bda1",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/0fbd1bdbec4f887bff071f86b450838a",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/03ae7aa0e2cf6aaedb6e1a3ac47ebdd8",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/f952a1776ccbe5458d35eb079a60d808",
                        "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/c9f8005aac083ffc035c07c32c908f80"],
                descImages=["https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/547087e0cbf3beb3c413d7a922fef275",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/5f587c274004a351cefc7362318bc92b",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/b2d6fafe36242f0badbc8135efd8f317",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/c5cd6d4da796436d39b22a0d89a4cc75",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/923dd72257832cacc2e6286052ce2b86",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/7b019206fa9c990a511f5cfba726816a",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/fbb0b858d1fb38ef373a207f27034756",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/faa29f57b1c1cff265630f36f983b3e7",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/02bfd8d19251f33a1215c87e205e7a52",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/3bda130cab8a7dac0bad9aa79ebd1d4b",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/3ad379cf4fb0962267a71dfca869ce0d",
                            "https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/30661717224fb26af5e1ca93d17bb80f"],
                goodsFrontImage="https://py-go.oss-cn-beijing.aliyuncs.com/goods_images/df392d01993cdab9de740fe17798bda1",
                isNew=1,
                isHot=0,
                onSale=1
            )
        )
        print("更新商品成功：", rsp)
    def all_category_list(self):
        rsp: goods_pb2.CategoryListResponse = self.stub.GetAllCategorysList(
            empty_pb2.Empty()
        )
        data = json.loads(rsp.jsonData)
        print("获取商品分类成功", data)
    def sub_category(self):
        rsp: goods_pb2.SubCategoryListResponse = self.stub.GetSubCategory(
            goods_pb2.CategoryListRequest(
                id=130370,
                level=2
            )
        )
        print("获取商品分类成功", rsp)

if __name__ == '__main__':
    Goods = GoodsTest()
    Goods.sub_category()
