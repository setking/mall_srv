import grpc

from common.register.consul import ConsulRegister
from user_srv.settings import settings
from user_srv.proto import user_pb2, user_pb2_grpc

# 用户接口测试
class UserTest:
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
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=3, pSize=2))
        print(rsp.total)
        for page in rsp.data:
            print(page.phone, page.birthDay)

    def update_user(self):
        rsq: user_pb2.UpdateUserInfo = self.stub.UpdateUser(
            user_pb2.UpdateUserInfo(id=2, nickName="test", gender="male", birthDay=1728144000))
        print(rsq)
if __name__ == '__main__':
    Users = UserTest()
    Users.user_list()