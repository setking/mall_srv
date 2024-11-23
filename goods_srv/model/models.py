from datetime import datetime

from playhouse.mysql_ext import JSONField
from peewee import  *
from goods_srv.settings import settings

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

class Category(BaseModel):
    name = CharField(max_length=20, verbose_name="名称")
    parent_category = ForeignKeyField("self", verbose_name="父类别", null=True)
    level = IntegerField(default=1, verbose_name="级别")
    is_tab = BooleanField(default=False, verbose_name="是否显示在首页")

# 品牌
class Brands(BaseModel):
    # id = AutoField(primary_key=True, verbose_name="id")
    name = CharField(max_length=50, verbose_name="名称", index=True, unique=True)
    logo = CharField(max_length=255,null=True, verbose_name="图标", default="")

# 商品
class Goods(BaseModel):
    category = ForeignKeyField(Category, verbose_name="商品类目", on_delete="CASCADE")
    brand = ForeignKeyField(Brands, verbose_name="所属品牌", on_delete="CASCADE")
    on_sale = BooleanField(default=True, verbose_name="是否上架")
    goods_sn = CharField(max_length=50,default="",verbose_name="商品唯一货号")
    name = CharField(max_length=100, verbose_name="商品名称")
    click_num = IntegerField(default=0, verbose_name="点击数")
    sold_num = IntegerField(default=0, verbose_name="销售量")
    fav_num = IntegerField(default=0, verbose_name="收藏数")
    market_price = FloatField(default=0, verbose_name="市场价格")
    shop_price = FloatField(default=0, verbose_name="本店价格")
    goods_brief = CharField(max_length=255, verbose_name="商品描述")
    ship_free = BooleanField(default=True, verbose_name="是否承担运费")
    images = JSONField(verbose_name="商品轮播图")
    desc_images = JSONField(verbose_name="详情页图片")
    goods_front_image = CharField(max_length=255, verbose_name="封面图")
    is_new = BooleanField(default=False, verbose_name="是否新品")
    is_hot = BooleanField(default=False, verbose_name="是否热门")

# 品牌分类
class GoodsCategoryBrand(BaseModel):
    id = AutoField(primary_key=True, verbose_name="id")
    category = ForeignKeyField(Category, verbose_name="类目")
    brand = ForeignKeyField(Brands, verbose_name="品牌")

    class Meta:
        indexes = (
            # 联合主键
            (("category", "brand"), True),
        )

# 轮播图
class Banner(BaseModel):
    image = CharField(max_length=255, default="", verbose_name="图片地址")
    url = CharField(max_length=255, default="", verbose_name="跳转地址")
    index = IntegerField(default=0, verbose_name="排序")
if __name__ == "__main__":
        settings.DB.create_tables([Category,Brands,Goods,GoodsCategoryBrand,Banner])
        # c1 = Category(name="test1", level=1)
        # c2 = Category(name="test2", level=2)
        # c1.save()
        # c2.save()
        # for c in Category.select():
        #     print(c.name, c.id)
        # c1 = Category.get(Category.id == 1)
        # c1.delete_instance(permanently=True)
        # Category.delete().where(Category.id == 2).execute()