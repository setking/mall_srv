import grpc
from loguru import logger

from userop_srv.model.models import UserFav
from userop_srv.proto import userfav_pb2, userfav_pb2_grpc
from google.protobuf import empty_pb2
from peewee import DoesNotExist


class UserFavServicer(userfav_pb2_grpc.UserFavServicer):
    # 收藏列表
    @logger.catch
    def GetFavList(self, request: userfav_pb2.UserFavRequest, context):
        rsp = userfav_pb2.UserFavListResponse()
        userfav = UserFav.select()
        if request.userId:
            try:
                userfav = UserFav.filter(UserFav.user == request.userId)
            except DoesNotExist:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("记录不存在")
                return userfav_pb2.UserFavListResponse()
        if request.goods:
            try:
                userfav = UserFav.filter(UserFav.goods == request.goods)
            except DoesNotExist:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("记录不存在")
                return userfav_pb2.UserFavListResponse()
        print(userfav)
        rsp.total = userfav.count()
        for fav in userfav:
            fav_rsp = userfav_pb2.UserFavResponse()
            fav_rsp.userId = fav.user
            fav_rsp.goods = fav.goods
            rsp.data.append(fav_rsp)
        return rsp

    # 添加收藏
    @logger.catch
    def AddUserFav(self, request: userfav_pb2.UserFavRequest, context):
        userfav = UserFav()
        userfav.user = request.userId
        userfav.goods = request.goods
        userfav.save(force_insert=True)
        return empty_pb2.Empty()
    # 删除收藏
    @logger.catch
    def DeleteUserFav(self, request: userfav_pb2.UserFavRequest, context):
        try:
            userfav = UserFav.get( UserFav.user == request.userId, UserFav.goods == request.goods)
            userfav.delete_instance(permanently=True)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()

    # 获取收藏状态
    @logger.catch
    def GetUserFavDetail(self, request: userfav_pb2.UserFavRequest, context):
        try:
            UserFav.get(UserFav.user == request.userId, UserFav.goods == request.goods)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()