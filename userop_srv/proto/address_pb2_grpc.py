# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import address_pb2 as address__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in address_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AddressStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateAddress = channel.unary_unary(
                '/Address/CreateAddress',
                request_serializer=address__pb2.AddressRequest.SerializeToString,
                response_deserializer=address__pb2.AddressResponse.FromString,
                _registered_method=True)
        self.GetAddress = channel.unary_unary(
                '/Address/GetAddress',
                request_serializer=address__pb2.AddressRequest.SerializeToString,
                response_deserializer=address__pb2.AddressListResponse.FromString,
                _registered_method=True)
        self.UpdateAddress = channel.unary_unary(
                '/Address/UpdateAddress',
                request_serializer=address__pb2.AddressRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.DeleteAddress = channel.unary_unary(
                '/Address/DeleteAddress',
                request_serializer=address__pb2.AddressRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)


class AddressServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateAddress(self, request, context):
        """添加地址
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAddress(self, request, context):
        """获取地址
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAddress(self, request, context):
        """更新地址
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAddress(self, request, context):
        """删除地址
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AddressServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateAddress': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAddress,
                    request_deserializer=address__pb2.AddressRequest.FromString,
                    response_serializer=address__pb2.AddressResponse.SerializeToString,
            ),
            'GetAddress': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAddress,
                    request_deserializer=address__pb2.AddressRequest.FromString,
                    response_serializer=address__pb2.AddressListResponse.SerializeToString,
            ),
            'UpdateAddress': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAddress,
                    request_deserializer=address__pb2.AddressRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DeleteAddress': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteAddress,
                    request_deserializer=address__pb2.AddressRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Address', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Address', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Address(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateAddress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Address/CreateAddress',
            address__pb2.AddressRequest.SerializeToString,
            address__pb2.AddressResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAddress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Address/GetAddress',
            address__pb2.AddressRequest.SerializeToString,
            address__pb2.AddressListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateAddress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Address/UpdateAddress',
            address__pb2.AddressRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteAddress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Address/DeleteAddress',
            address__pb2.AddressRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
