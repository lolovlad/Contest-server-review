from fastapi import Depends
from Classes.PathExtend import PathExtend

from ..Models import PostTask, Settings, UpdateTask
from ..database import get_session
from ..tables import Task
from ..Repositories import TaskRepository


class SettingsProtoServices:

    def __init__(self, repo_task: TaskRepository = Depends()):
        self.__repository: TaskRepository = repo_task

    async def settings_post(self, id: int, task: PostTask):
        name_folder = PathExtend.create_folder_name(10)
        folder = PathExtend(name_folder)
        folder.create_folder()

        task = Task(id=id,
                    time_work=task.time_work,
                    size_raw=task.size_raw,
                    type_input=task.type_input,
                    number_shipments=task.number_shipments,
                    path_files=name_folder)

        await self.__repository.add(task)

    async def settings_get(self, id: int) -> Settings:

        task = await self.__repository.get(id)

        list_files = PathExtend(task.path_files).list_file_in_folder()

        settings = Settings(id=task.id,
                            time_work=task.time_work,
                            size_raw=task.size_raw,
                            type_input=task.type_input,
                            type_output=task.type_output,
                            number_shipments=task.number_shipments,
                            name_file=list_files)
        return settings

    async def settings_delete(self, id_task: int):
        task: Task = await self.__repository.get(id_task)
        path = PathExtend(task.path_files)
        path.delete_dir()
        await self.__repository.delete(task)

    async def settings_update(self, update_task: UpdateTask):

        task: Task = await self.__repository.get(update_task.id)
        task.size_raw = update_task.size_raw
        task.type_input = update_task.type_input
        task.type_output = update_task.type_output
        task.number_shipments = update_task.number_shipments
        task.time_work = update_task.time_work
        await self.__repository.update(task)