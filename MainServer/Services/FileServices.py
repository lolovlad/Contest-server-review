from fastapi import Depends, UploadFile
from aiofiles import open

from Classes.PathExtend import PathExtend
from ..Repositories.TaskRepository import TaskRepository
from ..Repositories.FileBucketRepository import FileBucketRepository

from ..settings import settings


class FileServices:
    def __init__(self,
                 repo_task: TaskRepository = Depends(),
                 file_repo: FileBucketRepository = Depends()
                 ):
        self.__repo_task: TaskRepository = repo_task
        self.__file_repo: FileBucketRepository = file_repo

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

    async def upload_file_s3(self, id_task: int, file: UploadFile):
        task = await self.__repo_task.get(id_task)
        name, extend = file.filename.split(".")
        if extend == "json":
            file_key = f"{task.path_files}/setting.json"
        else:
            file_key = f"{task.path_files}/{file.filename}"
        content = await file.read()
        await self.__file_repo.upload_file(settings.minio_default_buckets,
                                           file_key,
                                           content,
                                           file.content_type)

    async def delete_file(self, id_task: int, filename: str):
        task = await self.__repo_task.get(id_task)

        await self.__file_repo.delete_file(settings.minio_default_buckets,
                                           f"{task.path_files}/{filename}")
