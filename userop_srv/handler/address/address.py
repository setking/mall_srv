import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist

from userop_srv.model.models import Address
from userop_srv.proto import address_pb2, address_pb2_grpc


class AddressServicer(address_pb2_grpc.AddressServicer):
    @logger.catch
    # 添加地址
    def CreateAddress(self, request: address_pb2.AddressRequest, context):
        address = Address()
        address.user = request.userId
        address.province = request.province
        address.city = request.city
        address.district = request.district
        address.address = request.address
        address.signer_name = request.signerName
        address.signer_phone = request.signerPhone
        address.save()
        rsp = address_pb2.AddressResponse(id=address.id)
        return rsp

    # 获取地址
    @logger.catch
    def GetAddress(self, request: address_pb2.AddressRequest, context):
        rsp = address_pb2.AddressListResponse()
        address = Address.select()
        if request.userId:
            address = Address.file(Address.user == request.userId)
        rsp.total = address.count()
        for local in address:
            address_rsp = address_pb2.AddressResponse()
            address_rsp.id = local.id
            address_rsp.userId = local.user
            address_rsp.province = local.province
            address_rsp.city = local.city
            address_rsp.district = local.district
            address_rsp.address = local.address
            address_rsp.signerName = local.signer_name
            address_rsp.signerPhone = local.signer_phone
            rsp.data.append(address_rsp)
        return rsp
    # 更新地址
    @logger.catch
    def UpdateAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(request.id)
            if request.province:
                address.province = request.province
            if request.city:
                address.city = request.city
            if request.district:
                address.district = request.district
            if request.address:
                address.address = request.address
            if request.signerName:
                address.signer_name = request.signerName
            if request.signerPhone:
                address.signer_phone = request.signerPhone
            address.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()

    # 删除地址
    @logger.catch
    def DeleteAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(request.id)
            address.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return  empty_pb2.Empty()