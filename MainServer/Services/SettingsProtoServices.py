from fastapi import Depends

from ..Models import PostTask, Settings, UpdateTask
from ..database import get_session
from ..tables import Task
from ..Repositories import TaskRepository
from ..Repositories.FileBucketRepository import FileBucketRepository
from ..settings import settings as settings_env


class SettingsProtoServices:

    def __init__(self,
                 repo_task: TaskRepository = Depends(),
                 repo_file: FileBucketRepository = Depends()):
        self.__repository: TaskRepository = repo_task
        self.__file_repo: FileBucketRepository = repo_file

    async def settings_post(self, id: int, task: PostTask):
        task = Task(id=id,
                    time_work=task.time_work,
                    size_raw=task.size_raw,
                    type_input=task.type_input,
                    number_shipments=task.number_shipments,
                    path_files=f"task_{id}")
        await self.__repository.add(task)

    async def settings_get(self, id: int) -> Settings:

        task = await self.__repository.get(id)

        files = await self.__file_repo.get_list_file(settings_env.minio_default_buckets,
                                                     f"{task.path_files}/")

        settings = Settings(id=task.id,
                            time_work=task.time_work,
                            size_raw=task.size_raw,
                            type_input=task.type_input,
                            type_output=task.type_output,
                            number_shipments=task.number_shipments,
                            name_file=files)
        return settings

    async def settings_delete(self, id_task: int):
        task: Task = await self.__repository.get(id_task)
        try:
            files = await self.__file_repo.get_list_file(settings_env.minio_default_buckets,
                                                         f"{task.path_files}/")
            for i in files:
                await self.__file_repo.delete_object(settings_env.minio_default_buckets,
                                                     f"{task.path_files}/{i}")
        except Exception:
            pass
        await self.__repository.delete(task)

    async def settings_update(self, update_task: UpdateTask):

        task: Task = await self.__repository.get(update_task.id)
        task.size_raw = update_task.size_raw
        task.type_input = update_task.type_input
        task.type_output = update_task.type_output
        task.number_shipments = update_task.number_shipments
        task.time_work = update_task.time_work
        await self.__repository.update(task)