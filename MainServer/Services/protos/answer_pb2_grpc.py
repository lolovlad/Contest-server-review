# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from MainServer.Services.protos import answer_pb2 as MainServer_dot_Models_dot_protos_dot_answer__pb2


class AnswerApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendAnswer = channel.unary_unary(
                '/AnswerApi/SendAnswer',
                request_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerRequest.SerializeToString,
                response_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerCodeResponse.FromString,
                )
        self.GetListAnswersTask = channel.unary_unary(
                '/AnswerApi/GetListAnswersTask',
                request_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskRequest.SerializeToString,
                response_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskResponse.FromString,
                )
        self.GetAnswersContest = channel.unary_unary(
                '/AnswerApi/GetAnswersContest',
                request_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestRequest.SerializeToString,
                response_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestResponse.FromString,
                )
        self.GetReportFile = channel.unary_unary(
                '/AnswerApi/GetReportFile',
                request_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileRequest.SerializeToString,
                response_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileResponse.FromString,
                )


class AnswerApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendAnswer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetListAnswersTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAnswersContest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReportFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnswerApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendAnswer': grpc.unary_unary_rpc_method_handler(
                    servicer.SendAnswer,
                    request_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerRequest.FromString,
                    response_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerCodeResponse.SerializeToString,
            ),
            'GetListAnswersTask': grpc.unary_unary_rpc_method_handler(
                    servicer.GetListAnswersTask,
                    request_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskRequest.FromString,
                    response_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskResponse.SerializeToString,
            ),
            'GetAnswersContest': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAnswersContest,
                    request_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestRequest.FromString,
                    response_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestResponse.SerializeToString,
            ),
            'GetReportFile': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReportFile,
                    request_deserializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileRequest.FromString,
                    response_serializer=MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AnswerApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AnswerApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendAnswer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AnswerApi/SendAnswer',
            MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerRequest.SerializeToString,
            MainServer_dot_Models_dot_protos_dot_answer__pb2.SendAnswerCodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetListAnswersTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AnswerApi/GetListAnswersTask',
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskRequest.SerializeToString,
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetListAnswersTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAnswersContest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AnswerApi/GetAnswersContest',
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestRequest.SerializeToString,
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetAnswersContestResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReportFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AnswerApi/GetReportFile',
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileRequest.SerializeToString,
            MainServer_dot_Models_dot_protos_dot_answer__pb2.GetReportFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
