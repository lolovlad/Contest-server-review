from .protos import jsonTest_pb2, jsonTest_pb2_grpc

from Classes.PathExtend import PathExtend
from ..Repositories import TaskRepository
from ..tables import Task
from ..Models.TaskTestSettings import FileTaskTest

from json import load


class TaskFileSettingsTestService(jsonTest_pb2_grpc.JsonTestApiServicer):

    def __init__(self):
        super().__init__()
        self.__repository: TaskRepository = TaskRepository()

    async def __find_json_file(self, path: PathExtend):
        for name in path.list_file_in_folder():
            if name.endswith("json"):
                return PathExtend(path.abs_path(), name)
        return ""

    async def __get_model_json(self, id_task: int):
        task = await self.__repository.get(id_task)
        path = PathExtend(task.path_files)
        filename = await self.__find_json_file(path)
        with open(filename.abs_path(), "r") as file:
            file_json = FileTaskTest(**load(file))
        return path, file_json

    async def GetAllSettingsTests(self, request, context):
        _, file_json = await self.__get_model_json(request.id)

        response = []
        for chunk in file_json.setting_tests:
            response.append(jsonTest_pb2.SettingsTests(
                limitation_variable=" ".join(chunk.settings_test.limitation_variable),
                necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
                check_type=chunk.settings_test.check_type,
            ))

        return jsonTest_pb2.GetAllSettingsTestsResponse(settings=response)

    async def GetChunkTest(self, request, context):
        path, file_json = await self.__get_model_json(request.id)

        list_type_chunk = list(filter(lambda x: x.type_test == request.type_test, file_json.setting_tests))
        chunk = list_type_chunk[request.index]

        settings_test = jsonTest_pb2.SettingsTests(
            limitation_variable=" ".join(chunk.settings_test.limitation_variable),
            necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
            check_type=chunk.settings_test.check_type,
        )

        list_test = []
        for test in chunk.tests:
            k = PathExtend(path.abs_path(), test.filling_type_variable).abs_path()
            list_test.append(jsonTest_pb2.Tests(
                score=test.score,
                filling_type_variable=open(PathExtend(path.abs_path(), test.filling_type_variable).abs_path(), "rb").read(),
                answer=open(PathExtend(path.abs_path(), test.answer).abs_path(), "rb").read()
            ))

        proto_chunk = jsonTest_pb2.ChunkTests(
            setting_tests=settings_test,
            tests=list_test
        )
        return proto_chunk
