import json

import nacos

# Both HTTP/HTTPS protocols are supported, if not set protocol prefix default is HTTP, and HTTPS with no ssl check(verify=False)
# "192.168.3.4:8848" or "https://192.168.3.4:443" or "http://192.168.3.4:8848,192.168.3.5:8848" or "https://192.168.3.4:443,https://192.168.3.5:443"
SERVER_ADDRESSES = "192.168.194.100:8848"
# 命名空间id
NAMESPACE = "fdb3061f-6415-4bd2-98a5-77b999d7a4e3"

# no auth mode
client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)
# auth mode
# client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, ak="{ak}", sk="{sk}")

# get config
data_id = "user-srv.json"
group = "dev"
data = client.get_config(data_id, group)
jsonData = json.loads(data)
print(jsonData)
def test_cb(args):
    print("配置文件变化")
    print(args)


if __name__ == "__main__":
    import time

    client.add_config_watcher(data_id, group, test_cb)
    time.sleep(3000)