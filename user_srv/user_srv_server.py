import os
import socket
import sys
import argparse
from loguru import logger
from functools import partial
import grpc
import signal
from concurrent import futures

BASE_URL = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(BASE_URL)
sys.path.insert(0, BASE_URL)
from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.handler.user import UserServicer
from common.grpc_health.v1 import health_pb2_grpc, health_pb2
from common.grpc_health.v1 import health
from common.register.consul import ConsulRegister
from user_srv.settings import settings


def on_exit(signo, frame, service_id):
    register = ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    logger.info(f"注销{service_id}服务")
    register.unregister(service_id)
    logger.info("注销成功")
    sys.exit(0)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default="121.43.157.170", help="IP address")
    parser.add_argument('--port', type=int, default=0, help="IP port")
    args = parser.parse_args()
    if args.port == 0:
        port = get_free_tcp_port()
    else:
        port = args.port
    logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 注册用户服务
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    # 注册健康检查
    health_service = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_service, server)
    server.add_insecure_port(f'[::]:{port}')
    # 主进程退出信号监听
    # win中断信号只支持ctrl+c和kill信号量（signal）
    import uuid
    service_id = str(uuid.uuid1())
    signal.signal(signal.SIGINT, partial(on_exit, service_id))
    signal.signal(signal.SIGTERM, partial(on_exit, service_id))
    logger.info(f"启动服务：{args.ip}:{port}")
    server.start()
    logger.info(f"服务注册开始")
    register = ConsulRegister(settings.CONSUL_HOST, settings.CONSUL_PORT)
    if not register.register_grpc(name=settings.SERVICE_NAME, id=service_id, tags=settings.SERVICE_TAGS,
                                  address=args.ip,
                                  port=port):
        sys.exit(0)
    server.wait_for_termination()


if __name__ == '__main__':
    settings.client.add_config_watcher(settings.NACOS["DataId"],settings.NACOS["Group"], settings.update_nacos) #这个逻辑必须放在这里，不然win会报错
    serve()
