import time

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from datetime import date
from peewee import *
from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    # 用户模型
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男")
    )
    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )
    phone = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_img = CharField(max_length=255, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=255, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="简介")
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="角色权限")

    class Meta:
        pass


if __name__ == "__main__":
    settings.DB.create_tables([User])

    # for i in range(10):
    #     user = User()
    #     user.nick_name = f"lily{i}"
    #     user.phone = f"1888888888{i}"
    #     user.password = pbkdf2_sha256.hash("admin123")
    #     user.save()
    users = User().select()
    users = users.limit(2).offset(3)
    for user in users:
        # print(user.phone)
        if user.birthday:
            # print(user.birthday)
            u_time = int(time.mktime(user.birthday.timetuple()))
            print(u_time)
        #     print(date.fromtimestamp(u_time))
