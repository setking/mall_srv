import time
from math import trunc

from loguru import logger
import grpc
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from peewee import DoesNotExist
from datetime import date
from user_srv.model.models import User
from user_srv.proto import user_pb2, user_pb2_grpc
from google.protobuf import empty_pb2


class UserServicer(user_pb2_grpc.UserServicer):
    def convert_user_to_rsp(self, user):
        # 将user的model对象转换成message对象
        user_info_rsp = user_pb2.UserInfoResponse()
        user_info_rsp.id = user.id
        user_info_rsp.password = user.password
        user_info_rsp.phone = user.phone
        user_info_rsp.role = user.role

        if user.nick_name:
            user_info_rsp.nickName = user.nick_name
        if user.gender:
            user_info_rsp.gender = user.gender
        if user.birthday:
            user_info_rsp.birthDay = int(time.mktime(user.birthday.timetuple()))

        return user_info_rsp

    @logger.catch
    def GetUserList(self, request: user_pb2.PageInfo, context):
        rsp = user_pb2.UserListResponse()
        users = User.select()
        rsp.total = users.count()
        print("注册用户服务")
        start = 0
        per_page_nums = 10
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            start = per_page_nums * (request.pn - 1)
        users = users.limit(per_page_nums).offset(start)
        for user in users:
            rsp.data.append(self.convert_user_to_rsp(user))
        return rsp

    @logger.catch
    def UpdateUser(self, request: user_pb2.PageInfo, context):
        # 更新用户信息
        try:
            user = User.get(User.id == request.id)
            user.nick_name = request.nickName
            user.gender = request.gender
            user.birthday = date.fromtimestamp(request.birthDay)
            user.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByPhone(self, request: user_pb2.PhoneRequest, context):
        # 通过mobile查询用户
        try:
            user = User.get(User.phone == request.phone)

            return self.convert_user_to_rsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CheckPassword(self, request: user_pb2.PasswordCheckInfo, context):
        return user_pb2.CheckResponse(success=pbkdf2_sha256.verify(request.password, request.encryptedPassword))

    @logger.catch
    def CreateUser(self,request: user_pb2.CreateUserInfo, context):
        # 注册新用户
        try:
            User.get(User.phone == request.phone)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("用户已存在")
            return user_pb2.UserInfoResponse()
        except DoesNotExist:
            pass
        user = User()
        user.nick_name = request.nickName
        user.phone = request.phone
        user.password = pbkdf2_sha256.hash(request.password)
        user.save()
        return self.convert_user_to_rsp(user)