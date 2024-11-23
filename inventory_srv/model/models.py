from datetime import datetime

from peewee import  *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

from inventory_srv.settings import settings


# class ReconnectMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
#     pass
# DB = ReconnectMySQLDatabase("mall_inventory_srv", host="192.168.194.100", port=3306, user="root", password="root")

#删除 - 物理删除和逻辑删除
class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now(), verbose_name="添加时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")
    update_time = DateTimeField(default=datetime.now(), verbose_name="更新时间")
    def save(self, *args, **kwargs):
        # 判断是新加的数据还是更新数据
        if self._pk is not None:
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self,permanently=False, recursive = False, delete_nullable = False):
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)
    class Meta:
        database = settings.DB
# # 仓库表
# class Stock(BaseModel):
#     name = CharField(verbose_name="仓库名称")
#     address = CharField(verbose_name="仓库地址")
#
# 库存表
class Inventory(BaseModel):
    goods = IntegerField(unique=True, verbose_name="商品id")
    stocks = IntegerField(default=0,verbose_name="库存数量")
    version = IntegerField(default=0, verbose_name="版本号")#分布式锁的乐观锁
# 库存商品信息
class InventoryHistory(BaseModel):
  order_sn = CharField(unique=True,max_length=20, verbose_name="订单id")
  order_inv_detail = CharField(max_length=200, verbose_name="订单详情")
  status = IntegerField(choices=((1, "已扣减"),(2, "已归还")), default=1, verbose_name="库存商品状态")

if __name__ == "__main__":
    settings.DB.create_tables([InventoryHistory])
    #生成Inventory表数据
    # for i in range(421, 841):
    #     try:
    #         inv = Inventory.get(Inventory.goods == i)
    #         inv.stocks = 100
    #         inv.save()
    #     except DoesNotExist as e:
    #         inv = Inventory(goods=i, stocks=100)
    #         inv.save(force_insert=True)