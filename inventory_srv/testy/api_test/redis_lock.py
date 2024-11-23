from random import randint

import grpc
from loguru import logger
from peewee import DoesNotExist
import time

from inventory_srv.settings import settings

from inventory_srv.model.models import Inventory
from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from google.protobuf import empty_pb2
import redis
import threading

class Lock:
    def __init__(self, name):
        self.redis_client = redis.Redis(host="192.168.194.100")
        self.name = name
    def acquire(self):
        if self.redis_client.setnx(self.name, 1):#如果不存在，则 SET
            return True
        else:
            time.sleep(1)
            self.acquire()
    def release(self):
        self.redis_client.delete(self.name)
def sell():
    goods_list = [(421, 1),(422, 2),(423, 3)]
    with settings.DB.atomic() as txn:
        for goods_id, num in goods_list:
            lock = Lock(f"lock:goods_{goods_id}")
            lock.acquire()
            goods_inv = Inventory.get(Inventory.goods == goods_id)
            print(f"商品{goods_id}售出{num}件")
            time.sleep(randint(1, 3))
            if goods_inv.stocks < num:
                print(f"商品{goods_id}库存不足")
                txn.rollback()#回滚事务
                return empty_pb2.Empty()
            else:
                query = Inventory.update(stocks=Inventory.stocks - num).where(Inventory.goods == goods_id)
                ok = query.execute()
                if ok:
                    print("更新成功")
                else:
                    print("更新失败")
            lock.release()
if __name__ == '__main__':
    t1 = threading.Thread(target=sell)
    t2 = threading.Thread(target=sell)
    t1.start()
    t2.start()
    t1.join()
    t2.join()