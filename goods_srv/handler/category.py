import json

import grpc
from envs.mall_srv.DLLs.unicodedata import category
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist

from goods_srv.model.models import Goods, Category, Brands
from goods_srv.proto import goods_pb2, goods_pb2_grpc


class CategoryServicer(goods_pb2_grpc.GoodsServicer):
  pass