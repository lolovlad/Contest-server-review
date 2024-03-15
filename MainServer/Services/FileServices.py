from fastapi import Depends, UploadFile
from aiofiles import open

from Classes.PathExtend import PathExtend
from ..Repositories.TaskRepository import TaskRepository


class FileServices:
    def __init__(self, repo_task: TaskRepository = Depends()):
        self.__repo_task: TaskRepository = repo_task

    async def upload_file(self, id_task: int, file: UploadFile):
        task = await self.__repo_task.get(id_task)
        name, extend = file.filename.split(".")
        if extend == "json":
            filepath = PathExtend(task.path_files)
            filepath.delete_files_in_folder(f".{extend}")

        filepath = PathExtend(task.path_files, file.filename)
        async with open(str(filepath), 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

    async def delete_file(self, id_task: int, filename: str):
        task = await self.__repo_task.get(id_task)
        filepath = PathExtend(task.path_files, filename)
        filepath.delete_file()
