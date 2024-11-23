import json

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist
from urllib3 import request

from goods_srv.model.models import Goods, Category, Brands, Banner, GoodsCategoryBrand
from goods_srv.proto import goods_pb2, goods_pb2_grpc


class GoodsServicer(goods_pb2_grpc.GoodsServicer):
    def category_model_to_dict(self, category):
        re = {}
        re["id"] = category.id
        re["name"] = category.name
        re["parent_id"] = category.parent_category_id
        re["level"] = category.level
        re["is_tab"] = category.is_tab
        return re
    def convert_model_to_model(self, model):
        info_rsp = goods_pb2.GoodsInfoResponse()

        info_rsp.id = model.id
        info_rsp.categoryId = model.category_id
        info_rsp.name = model.name
        info_rsp.goodsSn = model.goods_sn
        info_rsp.clickNum = model.click_num
        info_rsp.soldNum = model.sold_num
        info_rsp.favNum = model.fav_num
        info_rsp.marketPrice = model.market_price
        info_rsp.shopPrice = model.shop_price
        info_rsp.goodsBrief = model.goods_brief
        info_rsp.shipFree = model.ship_free
        info_rsp.images.extend(model.images)
        info_rsp.descImages.extend(model.desc_images)
        info_rsp.goodsFrontImage = model.goods_front_image
        info_rsp.isNew = model.is_new
        info_rsp.isHot = model.is_hot
        info_rsp.onSale = model.on_sale

        info_rsp.category.id = model.category.id
        info_rsp.category.name = model.category.name

        info_rsp.brand.id = model.brand.id
        info_rsp.brand.name = model.brand.name
        info_rsp.brand.logo = model.brand.logo
        return info_rsp
    @logger.catch
    # 查询所有商品
    def GoodsList(self, request: goods_pb2.GoodsFilterRequest, context):
        rsp = goods_pb2.GoodsListResponse()
        goods = Goods.select()
        if request.keyWords:
            goods = goods.filter(Goods.name.contains(request.keyWords))
        if request.isHot:
            goods = goods.filter(Goods.is_hot == True)
        if request.isNew:
            goods = goods.filter(Goods.is_new == True)
        if request.priceMin:
            goods = goods.filter(Goods.shop_price >= request.priceMin)
        if request.priceMax:
            goods = goods.filter(Goods.shop_price <= request.priceMax)
        if request.brand:
            goods = goods.filter(Goods.brand_id == request.brand)
        if request.topCategory:
            try:
                ids = []
                category = Category.get(Category.id == request.topCategory)
                level = category.level
                if level == 1:
                    cc = Category.alias()
                    categorys = Category.select().where(Category.parent_category_id.in_(
                        cc.select(cc.id).where(cc.parent_category_id == request.topCategory)))
                    for category in categorys:
                        ids.append(category.id)
                elif level == 2:
                    categorys = Category.select().where(Category.parent_category_id == request.topCategory)
                    for category in categorys:
                        ids.append(category.id)
                elif level == 3:
                    ids.append(request.topCategory)
                goods = goods.where(Goods.category_id.in_(ids))
            except Exception as e:
                pass
        # 分页 limit offset
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)
        rsp.total = goods.count()
        goods = goods.limit(per_page_nums).offset(start)
        for good in goods:
            rsp.data.append(self.convert_model_to_model(good))
        return rsp

    @logger.catch
    # ids查询商品
    def BatchGetGoods(self, request: goods_pb2.BatchGoodsIdInfo, context):
        print(f"id:{request.id}")
        try:
            rsp = goods_pb2.GoodsListResponse()
            goods = Goods.select().where(Goods.id.in_(list(request.id)))
            rsp.total = goods.count()
            for good in goods:
                rsp.data.append(self.convert_model_to_model(good))
            return rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品记录不存在")
            return goods_pb2.GoodsListResponse()

    @logger.catch
    # 删除商品
    def DeleteGoods(self, request: goods_pb2.DeleteGoodsInfo, context):
        try:
            goods = Goods.get(request.id)
            goods.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return empty_pb2.Empty()

    @logger.catch
    # 获取商品详情
    def GetGoodsDetail(self, request: goods_pb2.GoodInfoRequest, context):
        try:
            goods = Goods.get(Goods.id == request.id)
            #商品点击数
            goods.click_num += 1
            goods.save()
            return self.convert_model_to_model(goods)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return goods_pb2.GoodsInfoResponse()

    @logger.catch
    # 新建商品
    def CreateGoods(self, request: goods_pb2.CreateGoodsInfo, context):
        try:
            category = Category.get(Category.id == request.categoryId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品分类不存在")
            return goods_pb2.GoodsInfoResponse()
        try:
            brand = Brands.get(Brands.id == request.brandId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌不存在")
            return goods_pb2.GoodsInfoResponse()
        goods = Goods()
        goods.brand = brand
        goods.category = category
        goods.name = request.name
        goods.goods_sn = request.goodsSn
        goods.market_price = request.marketPrice
        goods.shop_price = request.shopPrice
        goods.goods_brief = request.goodsBrief
        goods.ship_free = request.shipFree
        goods.images = list(request.images)
        goods.desc_images = list(request.descImages)
        goods.goods_front_image = request.goodsFrontImage
        goods.is_new = request.isNew
        goods.is_hot = request.isHot
        goods.on_sale = request.onSale
        goods.save()
       # TODO 完善库存设置 - 分布式事务
        return self.convert_model_to_model(goods)

    @logger.catch
    # 更新商品
    def UpdateGoods(self, request: goods_pb2.CreateGoodsInfo, context):
        if request.categoryId:
            try:
                category = Category.get(Category.id == request.categoryId)
            except DoesNotExist as e:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("库存设置失败")
                return empty_pb2.Empty()
        if request.brandId:
            try:
                brand = Brands.get(Brands.id == request.brandId)
            except DoesNotExist as e:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("品牌不存在")
                return empty_pb2.Empty()
            try:
                goods = Goods.get(Goods.id == request.id)
            except DoesNotExist as e:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("商品不存在")
                return empty_pb2.Empty()
            if not request.categoryId:
                goods.is_new = request.isNew
                goods.is_hot = request.isHot
                goods.on_sale = request.onSale
            else:
                goods.brand = brand
                goods.category = category
                goods.name = request.name
                goods.goods_sn = request.goodsSn
                goods.market_price = request.marketPrice
                goods.shop_price = request.shopPrice
                goods.goods_brief = request.goodsBrief
                goods.ship_free = request.shipFree
                goods.images = list(request.images)
                goods.desc_images = list(request.descImages)
                goods.goods_front_image = request.goodsFrontImage
            goods.save()
            # TODO 完善库存设置 - 分布式事务
            return empty_pb2.Empty()
    @logger.catch
    # 商品分类
    def GetAllCategorysList(self, request: empty_pb2.Empty(), context):

        level1 = []
        level2 = []
        level3 = []
        category_list_rsp = goods_pb2.CategoryListResponse()
        category_list_rsp.total = Category.select().count()
        for category in Category.select():
            category_rsp = goods_pb2.CategoryInfoResponse()
            category_rsp.id = category.id
            category_rsp.name = category.name
            if category.parent_category_id:
                category_rsp.parentCategory = category.parent_category_id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab
            category_list_rsp.data.append(category_rsp)

            if category.level == 1:
                level1.append(self.category_model_to_dict(category))
            if category.level == 2:
                level2.append(self.category_model_to_dict(category))
            if category.level == 3:
                level3.append(self.category_model_to_dict(category))
        for data3 in level3:
            for data2 in level2:
                if data3["parent_id"] == data2["id"]:
                    if "sub_category" not in data2:
                        data2["sub_category"] = [data3]
                    else:
                        data2["sub_category"].append(data3)
        for data2 in level2:
            for data1 in level1:
                if data2["parent_id"] == data1["id"]:
                    if "sub_category" not in data1:
                        data1["sub_category"] = [data2]
                    else:
                        data1["sub_category"].append(data2)
        category_list_rsp.jsonData = json.dumps(level1)
        return category_list_rsp

    @logger.catch
    # 商品子分类
    def GetSubCategory(self, request: goods_pb2.CategoryListRequest, context):
        category_list_rsp = goods_pb2.SubCategoryListResponse()
        category_list_rsp.total = Category.select().count()
        try:
            category_info =  Category.get(Category.id == request.id)
            category_list_rsp.info.id = category_info.id
            category_list_rsp.info.name = category_info.name
            if category_info.parent_category_id:
                category_list_rsp.info.parentCategory = category_info.parent_category_id
            category_list_rsp.info.level = category_info.level
            category_list_rsp.info.isTab = category_info.is_tab
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("没有找到对应商品")
            return goods_pb2.SubCategoryListResponse()
        categorys = Category.select().where(Category.parent_category_id == request.id)
        category_list_rsp.total = categorys.count()
        for category in categorys:
            category_rsp = goods_pb2.CategoryInfoResponse()
            category_rsp.id = category.id
            category_rsp.name = category.name
            if category.parent_category_id:
                category_rsp.parentCategory = category.parent_category_id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab
            category_list_rsp.subCategorys.append(category_rsp)
        return category_list_rsp
    @logger.catch
    # 新建分类
    def CreateCategory(self, request: goods_pb2.CategoryInfoRequest, context):
        try:
            category = Category()
            category.name = request.name
            if request.level != 1:
                category.parent_category = request.parentCategory
            category.level = request.level
            category.is_tab = request.isTab
            category.save()
            category_rsp = goods_pb2.CategoryInfoResponse()
            category_rsp.id = category.id
            category_rsp.name = category.name
            if category.parent_category:
                category_rsp.parentCategory = category.parent_category.id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab
            return category_rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("数据插入失败")
            return goods_pb2.CategoryInfoResponse()


    @logger.catch
    # 删除分类
    def DeleteCategory(self, request: goods_pb2.DeleteCategoryRequest, context):
        try:
            category = Category.get(request.id)
            category.delete_instance()
            #TODO 是否删除关联的category下的其他商品分类
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("商品记录不存在")
            return empty_pb2.Empty()
    # 更新分类
    def UpdateCategory(self, request: goods_pb2.CategoryInfoRequest, context):
        try:
            category = Category.get(request.id)
            if request.name:
                category.name = request.name
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("商品记录不存在")
            return empty_pb2.Empty()
        if request.level:
            category.level = request.level
        if request.parentCategory:
            category.parent_category = request.parentCategory
        category.is_tab = request.isTab
        category.save()
        return empty_pb2.Empty()

    @logger.catch
    # 查询所有品牌logo
    def BrandList(self, request: goods_pb2.BrandFilterRequest, context):
        rsp = goods_pb2.BrandListResponse()
        brands = Brands.select()
        rsp.total = brands.count()
        for brand in brands:
            brand_rsp = goods_pb2.BrandInfoResponse()
            brand_rsp.id = brand.id
            brand_rsp.name = brand.name
            brand_rsp.logo = brand.logo
            rsp.data.append(brand_rsp)
        return rsp

    @logger.catch
    # 创建品牌logo
    def CreateBrand(self, request: goods_pb2.BrandRequest, context):

        try:
            brands = Brands.select().where(Brands.name == request.name)
            if brands:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("品牌记录已存在")
                return goods_pb2.BrandInfoResponse()
            brand = Brands()
            brand.name = request.name
            brand.logo = request.logo
            brand.save()
            brand_rsp = goods_pb2.BrandInfoResponse()
            brand_rsp.name = brand.name
            brand_rsp.logo = brand.logo
            return brand_rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("数据插入失败")
            return goods_pb2.BrandInfoResponse()

    @logger.catch
    # 删除品牌logo
    def DeleteBrand(self, request: goods_pb2.BrandRequest, context):
        try:
            brand = Brands.get(request.id)
            brand.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("品牌记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    # 更新品牌logo
    def UpdateBrand(self, request: goods_pb2.BrandRequest, context):
        try:
            brand = Brands.get(request.id)
            if request.name:
                brand.name = request.name
            if request.logo:
                brand.logo = request.logo
            brand.save()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("品牌记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    # 查询所有轮播图
    def BannerList(self, request:empty_pb2.Empty() , context):
        rsp = goods_pb2.BannerListResponse()
        banners = Banner.select()
        rsp.total = banners.count()
        for banner in banners:
            banner_rsp = goods_pb2.BannerResponse()
            banner_rsp.id = banner.id
            banner_rsp.index = banner.index
            banner_rsp.image = banner.image
            banner_rsp.url = banner.url
            rsp.data.append(banner_rsp)
        return rsp

    @logger.catch
    # 创建轮播图
    def CreateBanner(self, request: goods_pb2.BannerRequest, context):
        try:
            banner = Banner()
            banner.image =request.image
            banner.index = request.index
            banner.url = request.url
            banner.save()
            banner_rsp = goods_pb2.BannerResponse()
            banner_rsp.image = banner.image
            banner_rsp.id = banner.id
            banner_rsp.index = banner.index
            banner_rsp.url = banner.url
            return banner_rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("数据插入失败")
            return goods_pb2.BannerResponse()
    @logger.catch
    # 删除轮播图
    def DeleteBanner(self, request: goods_pb2.BannerRequest, context):
        try:
            banner = Banner.get(request.id)
            banner.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("轮播图记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    # 更新轮播图
    def UpdateBanner(self, request: goods_pb2.BannerRequest, context):
        try:
            banner = Banner.get(request.id)
            if request.image:
                banner.image = request.image
            if request.index:
                banner.index = request.index
            if request.url:
                banner.url = request.url
            banner.save()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("轮播图记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    # 查询所有品牌
    def CategoryBrandList(self, request: goods_pb2.CategoryBrandFilterRequest, context):
        rsp = goods_pb2.CategoryBrandListResponse()
        category_brand = GoodsCategoryBrand.select()
        # 分页 limit offset
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)
        rsp.total = category_brand.count()
        category_brand = category_brand.limit(per_page_nums).offset(start)
        for cb in category_brand:
            cb_rsp = goods_pb2.CategoryBrandResponse()
            cb_rsp.id = cb.id

            cb_rsp.brand.id = cb.brand.id
            cb_rsp.brand.name = cb.brand.name
            cb_rsp.brand.logo = cb.brand.logo

            cb_rsp.category.id = cb.category.id
            cb_rsp.category.name = cb.category.name
            cb_rsp.category.level = cb.category.level
            cb_rsp.category.parentCategory = cb.category.parent_category_id
            cb_rsp.category.isTab = cb.category.is_tab
            rsp.data.append(cb_rsp)
        return rsp

    @logger.catch
    # ids查询品牌
    def GetCategoryBrandList(self, request: goods_pb2.CategoryInfoRequest, context):
        try:
            rsp = goods_pb2.BrandListResponse()
            category = Category.get(request.id)
            cbs = GoodsCategoryBrand.select().where(GoodsCategoryBrand.category == category)
            rsp.total = cbs.count()
            for cb in cbs:
                cb_rsp = goods_pb2.BrandInfoResponse()
                cb_rsp.id = cb.brand.id
                cb_rsp.name = cb.brand.name
                cb_rsp.logo = cb.brand.logo
                rsp.data.append(cb_rsp)
            return rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌类别记录不存在")
            return goods_pb2.BrandListResponse()
    @logger.catch
    # 新建品牌
    def CreateCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        cbs = GoodsCategoryBrand()
        try:
            brand = Brands.get(Brands.id == request.brandId)
            cbs.brand = brand
            category = Category.get(Category.id == request.categoryId)
            cbs.category = category
            cbs.save()
            cbs_rsp = goods_pb2.CategoryBrandResponse()
            cbs_rsp.id = cbs.id
            return cbs_rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("品牌类别记录不存在")
            return goods_pb2.CategoryBrandResponse()
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("内部错误")
            return goods_pb2.CategoryBrandResponse()

    @logger.catch
    # 删除品牌
    def DeleteCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        try:
            cbs = GoodsCategoryBrand.get(request.id)
            cbs.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("品牌记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    # 更新品牌
    def UpdateCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        try:
            cbs = GoodsCategoryBrand.get(request.id)
            brand = Brands.get(request.brandId)
            cbs.brand = brand
            category = Category.get(request.categoryId)
            cbs.category = category
            cbs.save()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("商品记录不存在")
            return empty_pb2.Empty()