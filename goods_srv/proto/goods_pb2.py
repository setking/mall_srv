# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: goods.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'goods.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bgoods.proto\x1a\x1bgoogle/protobuf/empty.proto\"0\n\x13\x43\x61tegoryListRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05level\x18\x02 \x01(\x05\"e\n\x13\x43\x61tegoryInfoRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0eparentCategory\x18\x03 \x01(\x05\x12\r\n\x05level\x18\x04 \x01(\x05\x12\r\n\x05isTab\x18\x05 \x01(\x08\"#\n\x15\x44\x65leteCategoryRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"0\n\x14QueryCategoryRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"f\n\x14\x43\x61tegoryInfoResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0eparentCategory\x18\x03 \x01(\x05\x12\r\n\x05level\x18\x04 \x01(\x05\x12\r\n\x05isTab\x18\x05 \x01(\x08\"\\\n\x14\x43\x61tegoryListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12#\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x15.CategoryInfoResponse\x12\x10\n\x08jsonData\x18\x03 \x01(\t\"z\n\x17SubCategoryListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12#\n\x04info\x18\x02 \x01(\x0b\x32\x15.CategoryInfoResponse\x12+\n\x0csubCategorys\x18\x03 \x03(\x0b\x32\x15.CategoryInfoResponse\"@\n\x1a\x43\x61tegoryBrandFilterRequest\x12\r\n\x05pages\x18\x01 \x01(\x05\x12\x13\n\x0bpagePerNums\x18\x02 \x01(\x05\"3\n\rFilterRequest\x12\r\n\x05pages\x18\x01 \x01(\x05\x12\x13\n\x0bpagePerNums\x18\x02 \x01(\x05\"G\n\x14\x43\x61tegoryBrandRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\ncategoryId\x18\x02 \x01(\x05\x12\x0f\n\x07\x62randId\x18\x03 \x01(\x05\"o\n\x15\x43\x61tegoryBrandResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12!\n\x05\x62rand\x18\x02 \x01(\x0b\x32\x12.BrandInfoResponse\x12\'\n\x08\x63\x61tegory\x18\x03 \x01(\x0b\x32\x15.CategoryInfoResponse\"F\n\rBannerRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05index\x18\x02 \x01(\x05\x12\r\n\x05image\x18\x03 \x01(\t\x12\x0b\n\x03url\x18\x04 \x01(\t\"G\n\x0e\x42\x61nnerResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05index\x18\x02 \x01(\x05\x12\r\n\x05image\x18\x03 \x01(\t\x12\x0b\n\x03url\x18\x04 \x01(\t\"8\n\x12\x42randFilterRequest\x12\r\n\x05pages\x18\x01 \x01(\x05\x12\x13\n\x0bpagePerNums\x18\x02 \x01(\x05\"6\n\x0c\x42randRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04logo\x18\x03 \x01(\t\";\n\x11\x42randInfoResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04logo\x18\x03 \x01(\t\"D\n\x11\x42randListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12 \n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x12.BrandInfoResponse\"B\n\x12\x42\x61nnerListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x1d\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x0f.BannerResponse\"P\n\x19\x43\x61tegoryBrandListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12$\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x16.CategoryBrandResponse\"\x1e\n\x10\x42\x61tchGoodsIdInfo\x12\n\n\x02id\x18\x01 \x03(\x05\"\x1d\n\x0f\x44\x65leteGoodsInfo\x12\n\n\x02id\x18\x01 \x01(\x05\"5\n\x19\x43\x61tegoryBriefInfoResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\"2\n\x15\x43\x61tegoryFilterRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05isTab\x18\x02 \x01(\x08\"\x1d\n\x0fGoodInfoRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\xbd\x02\n\x0f\x43reateGoodsInfo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07goodsSn\x18\x03 \x01(\t\x12\x0e\n\x06stocks\x18\x07 \x01(\x05\x12\x13\n\x0bmarketPrice\x18\x08 \x01(\x02\x12\x11\n\tshopPrice\x18\t \x01(\x02\x12\x12\n\ngoodsBrief\x18\n \x01(\t\x12\x11\n\tgoodsDesc\x18\x0b \x01(\t\x12\x10\n\x08shipFree\x18\x0c \x01(\x08\x12\x0e\n\x06images\x18\r \x03(\t\x12\x12\n\ndescImages\x18\x0e \x03(\t\x12\x17\n\x0fgoodsFrontImage\x18\x0f \x01(\t\x12\r\n\x05isNew\x18\x10 \x01(\x08\x12\r\n\x05isHot\x18\x11 \x01(\x08\x12\x0e\n\x06onSale\x18\x12 \x01(\x08\x12\x12\n\ncategoryId\x18\x13 \x01(\x05\x12\x0f\n\x07\x62randId\x18\x14 \x01(\x05\"3\n\x12GoodsReduceRequest\x12\x0f\n\x07GoodsId\x18\x01 \x01(\x05\x12\x0c\n\x04nums\x18\x02 \x01(\x05\"L\n\x18\x42\x61tchCategoryInfoRequest\x12\n\n\x02id\x18\x01 \x03(\x05\x12\x11\n\tgoodsNums\x18\x02 \x01(\x05\x12\x11\n\tbrandNums\x18\x03 \x01(\x05\"\xbf\x01\n\x12GoodsFilterRequest\x12\x10\n\x08priceMin\x18\x01 \x01(\x05\x12\x10\n\x08priceMax\x18\x02 \x01(\x05\x12\r\n\x05isHot\x18\x03 \x01(\x08\x12\r\n\x05isNew\x18\x04 \x01(\x08\x12\r\n\x05isTab\x18\x05 \x01(\x08\x12\x13\n\x0btopCategory\x18\x06 \x01(\x05\x12\r\n\x05pages\x18\x07 \x01(\x05\x12\x13\n\x0bpagePerNums\x18\x08 \x01(\x05\x12\x10\n\x08keyWords\x18\t \x01(\t\x12\r\n\x05\x62rand\x18\n \x01(\x05\"\xb3\x03\n\x11GoodsInfoResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\ncategoryId\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07goodsSn\x18\x04 \x01(\t\x12\x10\n\x08\x63lickNum\x18\x05 \x01(\x05\x12\x0f\n\x07soldNum\x18\x06 \x01(\x05\x12\x0e\n\x06\x66\x61vNum\x18\x07 \x01(\x05\x12\x13\n\x0bmarketPrice\x18\t \x01(\x02\x12\x11\n\tshopPrice\x18\n \x01(\x02\x12\x12\n\ngoodsBrief\x18\x0b \x01(\t\x12\x11\n\tgoodsDesc\x18\x0c \x01(\t\x12\x10\n\x08shipFree\x18\r \x01(\x08\x12\x0e\n\x06images\x18\x0e \x03(\t\x12\x12\n\ndescImages\x18\x0f \x03(\t\x12\x17\n\x0fgoodsFrontImage\x18\x10 \x01(\t\x12\r\n\x05isNew\x18\x11 \x01(\x08\x12\r\n\x05isHot\x18\x12 \x01(\x08\x12\x0e\n\x06onSale\x18\x13 \x01(\x08\x12\x0f\n\x07\x61\x64\x64Time\x18\x14 \x01(\x03\x12,\n\x08\x63\x61tegory\x18\x15 \x01(\x0b\x32\x1a.CategoryBriefInfoResponse\x12!\n\x05\x62rand\x18\x16 \x01(\x0b\x32\x12.BrandInfoResponse\"D\n\x11GoodsListResponse\x12\r\n\x05total\x18\x01 \x01(\x05\x12 \n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x12.GoodsInfoResponse2\xaf\x0b\n\x05Goods\x12\x34\n\tGoodsList\x12\x13.GoodsFilterRequest\x1a\x12.GoodsListResponse\x12\x36\n\rBatchGetGoods\x12\x11.BatchGoodsIdInfo\x1a\x12.GoodsListResponse\x12\x33\n\x0b\x43reateGoods\x12\x10.CreateGoodsInfo\x1a\x12.GoodsInfoResponse\x12\x37\n\x0b\x44\x65leteGoods\x12\x10.DeleteGoodsInfo\x1a\x16.google.protobuf.Empty\x12\x37\n\x0bUpdateGoods\x12\x10.CreateGoodsInfo\x1a\x16.google.protobuf.Empty\x12\x36\n\x0eGetGoodsDetail\x12\x10.GoodInfoRequest\x1a\x12.GoodsInfoResponse\x12\x44\n\x13GetAllCategorysList\x12\x16.google.protobuf.Empty\x1a\x15.CategoryListResponse\x12@\n\x0eGetSubCategory\x12\x14.CategoryListRequest\x1a\x18.SubCategoryListResponse\x12=\n\x0e\x43reateCategory\x12\x14.CategoryInfoRequest\x1a\x15.CategoryInfoResponse\x12@\n\x0e\x44\x65leteCategory\x12\x16.DeleteCategoryRequest\x1a\x16.google.protobuf.Empty\x12>\n\x0eUpdateCategory\x12\x14.CategoryInfoRequest\x1a\x16.google.protobuf.Empty\x12\x34\n\tBrandList\x12\x13.BrandFilterRequest\x1a\x12.BrandListResponse\x12\x30\n\x0b\x43reateBrand\x12\r.BrandRequest\x1a\x12.BrandInfoResponse\x12\x34\n\x0b\x44\x65leteBrand\x12\r.BrandRequest\x1a\x16.google.protobuf.Empty\x12\x34\n\x0bUpdateBrand\x12\r.BrandRequest\x1a\x16.google.protobuf.Empty\x12\x39\n\nBannerList\x12\x16.google.protobuf.Empty\x1a\x13.BannerListResponse\x12/\n\x0c\x43reateBanner\x12\x0e.BannerRequest\x1a\x0f.BannerResponse\x12\x36\n\x0c\x44\x65leteBanner\x12\x0e.BannerRequest\x1a\x16.google.protobuf.Empty\x12\x36\n\x0cUpdateBanner\x12\x0e.BannerRequest\x1a\x16.google.protobuf.Empty\x12L\n\x11\x43\x61tegoryBrandList\x12\x1b.CategoryBrandFilterRequest\x1a\x1a.CategoryBrandListResponse\x12@\n\x14GetCategoryBrandList\x12\x14.CategoryInfoRequest\x1a\x12.BrandListResponse\x12\x44\n\x13\x43reateCategoryBrand\x12\x15.CategoryBrandRequest\x1a\x16.CategoryBrandResponse\x12\x44\n\x13\x44\x65leteCategoryBrand\x12\x15.CategoryBrandRequest\x1a\x16.google.protobuf.Empty\x12\x44\n\x13UpdateCategoryBrand\x12\x15.CategoryBrandRequest\x1a\x16.google.protobuf.EmptyB\tZ\x07.;protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'goods_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\007.;proto'
  _globals['_CATEGORYLISTREQUEST']._serialized_start=44
  _globals['_CATEGORYLISTREQUEST']._serialized_end=92
  _globals['_CATEGORYINFOREQUEST']._serialized_start=94
  _globals['_CATEGORYINFOREQUEST']._serialized_end=195
  _globals['_DELETECATEGORYREQUEST']._serialized_start=197
  _globals['_DELETECATEGORYREQUEST']._serialized_end=232
  _globals['_QUERYCATEGORYREQUEST']._serialized_start=234
  _globals['_QUERYCATEGORYREQUEST']._serialized_end=282
  _globals['_CATEGORYINFORESPONSE']._serialized_start=284
  _globals['_CATEGORYINFORESPONSE']._serialized_end=386
  _globals['_CATEGORYLISTRESPONSE']._serialized_start=388
  _globals['_CATEGORYLISTRESPONSE']._serialized_end=480
  _globals['_SUBCATEGORYLISTRESPONSE']._serialized_start=482
  _globals['_SUBCATEGORYLISTRESPONSE']._serialized_end=604
  _globals['_CATEGORYBRANDFILTERREQUEST']._serialized_start=606
  _globals['_CATEGORYBRANDFILTERREQUEST']._serialized_end=670
  _globals['_FILTERREQUEST']._serialized_start=672
  _globals['_FILTERREQUEST']._serialized_end=723
  _globals['_CATEGORYBRANDREQUEST']._serialized_start=725
  _globals['_CATEGORYBRANDREQUEST']._serialized_end=796
  _globals['_CATEGORYBRANDRESPONSE']._serialized_start=798
  _globals['_CATEGORYBRANDRESPONSE']._serialized_end=909
  _globals['_BANNERREQUEST']._serialized_start=911
  _globals['_BANNERREQUEST']._serialized_end=981
  _globals['_BANNERRESPONSE']._serialized_start=983
  _globals['_BANNERRESPONSE']._serialized_end=1054
  _globals['_BRANDFILTERREQUEST']._serialized_start=1056
  _globals['_BRANDFILTERREQUEST']._serialized_end=1112
  _globals['_BRANDREQUEST']._serialized_start=1114
  _globals['_BRANDREQUEST']._serialized_end=1168
  _globals['_BRANDINFORESPONSE']._serialized_start=1170
  _globals['_BRANDINFORESPONSE']._serialized_end=1229
  _globals['_BRANDLISTRESPONSE']._serialized_start=1231
  _globals['_BRANDLISTRESPONSE']._serialized_end=1299
  _globals['_BANNERLISTRESPONSE']._serialized_start=1301
  _globals['_BANNERLISTRESPONSE']._serialized_end=1367
  _globals['_CATEGORYBRANDLISTRESPONSE']._serialized_start=1369
  _globals['_CATEGORYBRANDLISTRESPONSE']._serialized_end=1449
  _globals['_BATCHGOODSIDINFO']._serialized_start=1451
  _globals['_BATCHGOODSIDINFO']._serialized_end=1481
  _globals['_DELETEGOODSINFO']._serialized_start=1483
  _globals['_DELETEGOODSINFO']._serialized_end=1512
  _globals['_CATEGORYBRIEFINFORESPONSE']._serialized_start=1514
  _globals['_CATEGORYBRIEFINFORESPONSE']._serialized_end=1567
  _globals['_CATEGORYFILTERREQUEST']._serialized_start=1569
  _globals['_CATEGORYFILTERREQUEST']._serialized_end=1619
  _globals['_GOODINFOREQUEST']._serialized_start=1621
  _globals['_GOODINFOREQUEST']._serialized_end=1650
  _globals['_CREATEGOODSINFO']._serialized_start=1653
  _globals['_CREATEGOODSINFO']._serialized_end=1970
  _globals['_GOODSREDUCEREQUEST']._serialized_start=1972
  _globals['_GOODSREDUCEREQUEST']._serialized_end=2023
  _globals['_BATCHCATEGORYINFOREQUEST']._serialized_start=2025
  _globals['_BATCHCATEGORYINFOREQUEST']._serialized_end=2101
  _globals['_GOODSFILTERREQUEST']._serialized_start=2104
  _globals['_GOODSFILTERREQUEST']._serialized_end=2295
  _globals['_GOODSINFORESPONSE']._serialized_start=2298
  _globals['_GOODSINFORESPONSE']._serialized_end=2733
  _globals['_GOODSLISTRESPONSE']._serialized_start=2735
  _globals['_GOODSLISTRESPONSE']._serialized_end=2803
  _globals['_GOODS']._serialized_start=2806
  _globals['_GOODS']._serialized_end=4261
# @@protoc_insertion_point(module_scope)
