import requests

headers = {"Content-Type": "application/json"}


# 注册健康检查
def register(name, id, address, port):
    url = "http://192.168.194.100:8500/v1/agent/service/register"
    # 注册http健康检查参数
    # rsp = requests.put(url, headers=headers, json={
    #     "Name": name,
    #     "ID": id,
    #     "Tags": ["mallWeb", "web"],
    #     "Address": address,
    #     "Port": port,
    #     "enableTagOverride": True,
    #     "Check": {
    #         "HTTP": f"http://{address}:{port}/health",
    #         "Interval": "10s",
    #         "Timeout": "5s",
    #         "status": "passing",
    #         "DeregisterCriticalServiceAfter": "15s"
    #     }
    # })
    # 注册grpc健康检查参数
    rsp = requests.put(url, headers=headers, json={
        "Name": name,
        "ID": id,
        "Tags": ["mallWeb", "web"],
        "Address": address,
        "Port": port,
        "enableTagOverride": True,
        "Check": {
            "GRPC": f"{address}:{port}",
            # GRPCUseTLS表示是否需要证书访问
            "GRPCUseTLS": False,
            "Interval": "10s",
            "Timeout": "5s",
            "status": "passing",
            "DeregisterCriticalServiceAfter": "15s"
        }
    })
    print(f"http://{address}:{port}/health")
    if rsp.status_code == 200:
        print("注册成功")
    else:
        print(f"注册失败:{rsp.status_code}")


# 注销健康检查
def un_register(service_name):
    url = f"http://192.168.194.100:8500/v1/agent/service/deregister/{service_name}"
    rsp = requests.put(url, headers=headers)
    if rsp.status_code == 200:
        print("注销成功")
    else:
        print(f"注销失败:{rsp.status_code}")
# 过滤服务
def filter_service(name):
    url = "http://192.168.194.100:8500/v1/agent/services"
    params = {
        "filter": f'Service =="{name}"'
    }
    rsp = requests.get(url=url, params=params).json()
    for k,v in rsp.items():
        print(k, v)
    # print(rsp)
if __name__ == "__main__":
    register("mallSrv", "mallSrv", "192.168.0.102", 50052)
    # un_register()
    # filter_service("mallSrv")
