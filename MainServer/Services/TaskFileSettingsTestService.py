from fastapi import Depends
from ..Models import SettingsTest, Test, ChunkTest, SettingsTestStr, ChunkTestReturn

from ..Repositories import TaskRepository, FileBucketRepository
from ..tables import Task
from ..Models.TaskTestSettings import FileTaskTest

from ..settings import settings

from json import loads


class TaskFileSettingsTestService:
    def __init__(self,
                 repo_task: TaskRepository = Depends(),
                 repo_file: FileBucketRepository = Depends()):
        self.__repository: TaskRepository = repo_task
        self.__repo_file: FileBucketRepository = repo_file

    async def __get_model_json(self, id_task: int):
        task = await self.__repository.get(id_task)
        data = await self.__repo_file.get_file(settings.minio_default_buckets,
                                               f"{task.path_files}/setting.json")
        file_json = FileTaskTest(**loads(data))
        path = f"{task.path_files}/"
        return path, file_json

    async def get_all_settings_tests(self, id: int) -> list[SettingsTestStr]:
        _, file_json = await self.__get_model_json(id)

        response = []
        for chunk in file_json.setting_tests:
            response.append(SettingsTestStr(
                limitation_variable=" ".join(chunk.settings_test.limitation_variable),
                necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
                check_type=chunk.settings_test.check_type,
            ))

        return response

    async def get_chunk_test(self, id: int, type_test: str, index: int) -> ChunkTestReturn:
        path, file_json = await self.__get_model_json(id)

        list_type_chunk = list(filter(lambda x: x.type_test == type_test, file_json.setting_tests))
        chunk = list_type_chunk[index]

        settings_test = SettingsTestStr(
            limitation_variable=" ".join(chunk.settings_test.limitation_variable),
            necessary_test=" ".join(map(str, chunk.settings_test.necessary_test)),
            check_type=chunk.settings_test.check_type,
        )

        list_test = []
        for test in chunk.tests:

            input_test = await self.__repo_file.get_file(settings.minio_default_buckets,
                                                         f"{path}{test.filling_type_variable}")

            output_test = await self.__repo_file.get_file(settings.minio_default_buckets,
                                                          f"{path}{test.answer}")

            list_test.append(Test(
                score=test.score,
                filling_type_variable=input_test.decode("utf-8"),
                answer=output_test.decode("utf-8")
            ))

        proto_chunk = ChunkTestReturn(
            settings_test=settings_test,
            tests=list_test
        )
        return proto_chunk
