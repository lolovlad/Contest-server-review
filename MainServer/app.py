from concurrent import futures
from grpc import aio

from MainServer.Services.protos import file_pb2_grpc
from MainServer.Services.protos import settings_pb2_grpc
from MainServer.Services.protos import jsonTest_pb2_grpc
from MainServer.Services.protos import compiler_pb2_grpc
from MainServer.Services.protos import answer_pb2_grpc
from MainServer.Services.protos import contest_pb2_grpc

from MainServer.Services.FileProtoServices import FileProtoService
from MainServer.Services.SettingsProtoServices import SettingsProtoServices
from MainServer.Services.TaskFileSettingsTestService import TaskFileSettingsTestService
from MainServer.Services.CompilerServices import CompilerServices
from MainServer.Services.AnswersServices import AnswersServices
from MainServer.Services.ContestServices import ContestServices

from .settings import settings

cleanup_coroutines = []


async def serve():
    server = aio.server()

    file_pb2_grpc.add_FileApiServicer_to_server(FileProtoService(), server)
    settings_pb2_grpc.add_SettingsApiServicer_to_server(SettingsProtoServices(), server)
    jsonTest_pb2_grpc.add_JsonTestApiServicer_to_server(TaskFileSettingsTestService(), server)
    compiler_pb2_grpc.add_CompilerApiServicer_to_server(CompilerServices(), server)
    answer_pb2_grpc.add_AnswerApiServicer_to_server(AnswersServices(), server)
    contest_pb2_grpc.add_ContestApiServicer_to_server(ContestServices(), server)

    server.add_insecure_port(f'{settings.server_host}:{settings.server_port}')
    print("start_server")
    await server.start()

    async def server_graceful_shutdown():
        await server.stop(5)

    cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()