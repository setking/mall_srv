from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
import nacos
import json
import redis
from loguru import logger

class ReconnectMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass

NACOS = {
    "Host": "192.168.194.100",
    "Port": 8848,
    "NameSpace": "67a5226e-b6ee-49c8-bcf8-67749dcc131c",
    "User": "nacos",
    "password": "nacos",
    "DataId": "inventory_srv",
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

ROCKETMQ_HOST = data["rocketmq"]["host"]
ROCKETMQ_PORT = data["rocketmq"]["port"]
#redis相关配置
REDIS_HOST = data["redis"]["host"]
REDIS_PORT = data["redis"]["port"]
REDIS_DB = data["redis"]["db"]
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,db=REDIS_DB)
REDIS_CLIENT = redis.StrictRedis(connection_pool=pool)
DB = ReconnectMySQLDatabase(data["mysql"]["db"], host=data["mysql"]["host"],
                            port=data["mysql"]["port"], user=data["mysql"]["user"],
                            password=data["mysql"]["password"])
