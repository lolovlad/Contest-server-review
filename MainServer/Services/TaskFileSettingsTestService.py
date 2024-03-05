from fastapi import Depends
from Classes.PathExtend import PathExtend
from ..Models import SettingsTest, Test, ChunkTest

from ..Repositories import TaskRepository
from ..tables import Task
from ..Models.TaskTestSettings import FileTaskTest

from json import load


class TaskFileSettingsTestService:
    def __init__(self, repo_task: TaskRepository = Depends()):
        self.__repository: TaskRepository = repo_task

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

    async def get_all_settings_tests(self, id: int) -> list[SettingsTest]:
        _, file_json = await self.__get_model_json(id)

        response = []
        for chunk in file_json.setting_tests:
            response.append(SettingsTest(
                limitation_variable=" ".join(chunk.settings_test.limitation_variable),
                necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
                check_type=chunk.settings_test.check_type,
            ))

        return response

    async def get_chunk_test(self, id: int, type_test: int, index: int) -> ChunkTest:
        path, file_json = await self.__get_model_json(id)

        list_type_chunk = list(filter(lambda x: x.type_test == type_test, file_json.setting_tests))
        chunk = list_type_chunk[index]

        settings_test = SettingsTest(
            limitation_variable=" ".join(chunk.settings_test.limitation_variable),
            necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
            check_type=chunk.settings_test.check_type,
        )

        list_test = []
        for test in chunk.tests:
            k = PathExtend(path.abs_path(), test.filling_type_variable).abs_path()
            list_test.append(Test(
                score=test.score,
                filling_type_variable=open(PathExtend(path.abs_path(), test.filling_type_variable).abs_path(), "rb").read(),
                answer=open(PathExtend(path.abs_path(), test.answer).abs_path(), "rb").read()
            ))

        proto_chunk = ChunkTest(
            setting_tests=settings_test,
            tests=list_test
        )
        return proto_chunk
