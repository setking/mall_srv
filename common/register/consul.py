from loguru import logger

from common.register.base import Register
import requests
import random

headers = {"Content-Type": "application/json"}


class ConsulRegister(Register):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def register(self, name, id, address, port, tags) -> bool:
        url = f"http://{self.host}:{self.port}/v1/agent/service/register"
        # 注册grpc健康检查参数
        rsp = requests.put(url, headers=headers, json={
            "Name": name,
            "ID": id,
            "Tags": tags,
            "Address": address,
            "Port": port,
            "enableTagOverride": True,
            "Check": {
                "HTTP": f"http://{address}:{port}/health",
                "Interval": "2s",
                "Timeout": "2s",
                "status": "passing",
                "DeregisterCriticalServiceAfter": "5s"
            }
        })
        logger.info(f"http://{address}:{port}/health")
        if rsp.status_code == 200:
            logger.info("GRPC健康检查服务注册成功")
            return True
        else:
            logger.error(f"GRPC健康检查服务注册失败:{rsp.status_code}")
            return False

    def register_grpc(self, name, id, address, port, tags) -> bool:
        url = f"http://{self.host}:{self.port}/v1/agent/service/register"
        # 注册http健康检查参数
        rsp = requests.put(url, headers=headers, json={
            "Name": name,
            "ID": id,
            "Tags": tags,
            "Address": address,
            "Port": port,
            "enableTagOverride": True,
            "Check": {
                "GRPC": f"{address}:{port}",
                # GRPCUseTLS表示是否需要证书访问
                "GRPCUseTLS": False,
                "Interval": "2s",
                "Timeout": "2s",
                "status": "passing",
                "DeregisterCriticalServiceAfter": "5s"
            }
        })
        logger.info(f"http://{address}:{port}/health")
        if rsp.status_code == 200:
            logger.info("HTTP健康检查服务注册成功")
            return True
        else:
            logger.error(f"HTTP健康检查服务注册失败:{rsp.status_code}")
            return False

    def unregister(self, service_id):
        url = f"http://{self.host}:{self.port}/v1/agent/service/deregister/{service_id}"
        rsp = requests.put(url, headers=headers)
        if rsp.status_code == 200:
            logger.info("注销成功")
        else:
            logger.error(f"注销失败:{rsp.status_code}")

    def get_all_services(self):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        rsp = requests.get(url=url).json()
        for k, v in rsp.items():
            logger.info(k, v)

    def filter_service(self, service):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": f'Service =="{service}"'
        }
        rsp = requests.get(url=url, params=params).json()
        # for k, v in rsp.items():
        #     logger.info(k, v)
        return rsp
    def filter_host_port(self, filter):
        if filter:
            service_info = random.choice(list(filter.values()))
            return service_info["Address"], service_info["Port"]
        return None, None