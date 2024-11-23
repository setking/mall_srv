from userop_srv.model.models import LeavingMessages
from userop_srv.proto import message_pb2, message_pb2_grpc
from loguru import logger


class MessageServicer(message_pb2_grpc.MessageServicer):
    @logger.catch
    #获取留言列表
    def MessageList(self, request: message_pb2.MessageRequest, context):
        rsp = message_pb2.MessageListResponse()
        messages = LeavingMessages.select()
        if request.userId:
            messages = LeavingMessages.file(LeavingMessages.user == request.userId)
        rsp.total = messages.count()
        for message in messages:
            message_rsp = message_pb2.MessageResponse()
            message_rsp.id = message.id
            message_rsp.userId = message.user
            message_rsp.messageType = message.message_type
            message_rsp.subject = message.subject
            message_rsp.message = message.message
            message_rsp.file = message.file
            rsp.data.append(message_rsp)
        return rsp

    @logger.catch
    def CreateMessage(self, request: message_pb2.MessageRequest, context):
        message = LeavingMessages()
        message.user = request.userId
        message.message_type = request.messageType
        message.subject = request.subject
        message.message = request.message
        message.file = request.file
        message.save()
        rsp = message_pb2.MessageResponse()
        rsp.id = message.id
        rsp.userId = message.user
        rsp.messageType = message.message_type
        rsp.subject = message.subject
        rsp.message = message.message
        rsp.file = message.file
        return rsp