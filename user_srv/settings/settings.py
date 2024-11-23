from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
import nacos
import json
from loguru import logger

class ReconnectMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass

NACOS = {
    "Host": "192.168.194.100",
    "Port": 8848,
    "NameSpace": "d10495e4-2032-47ff-8708-c5dc722b5f4f",
    "User": "nacos",
    "password": "nacos",
    "DataId": "user_srv",
    "Group": "dev"
}

client = nacos.NacosClient(f'{NACOS["Host"]}:{NACOS["Port"]}', namespace=NACOS["NameSpace"], username=NACOS["User"], password=NACOS["password"])
data = client.get_config(NACOS["DataId"], NACOS["Group"])
data = json.loads(data)

def update_nacos(args):
    global data
    print("更新nacos配置信息成功", args)
    data = json.loads(args["raw_content"])


# consul配置
CONSUL_HOST = data["consul"]["host"]
CONSUL_PORT = data["consul"]["port"]
# consul服务配置
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]
DB = ReconnectMySQLDatabase(data["mysql"]["db"], host=data["mysql"]["host"],
                            port=data["mysql"]["port"], user=data["mysql"]["user"],
                            password=data["mysql"]["password"])
