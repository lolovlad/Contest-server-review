from fastapi import Depends
from ..settings import settings
from Classes.PathExtend import PathExtend
from ..tables import Task
from ..Repositories import TaskRepository


class FileProtoService:

    def __init__(self, repo_task: TaskRepository = Depends()):
        self.__repository: TaskRepository = repo_task

    async def upload_file(self):
        pass
        '''data = bytearray()
        filepath = settings.static_path
        async for request in request_iterator:
            if request.metadata.name and request.metadata.extend:
                task = await self.__repository.get(request.metadata.id_task)
                if request.metadata.extend == "json":
                    filepath = PathExtend(task.path_files)
                    filepath.delete_files_in_folder(f".{request.metadata.extend}")
                file_name = f"{request.metadata.name}.{request.metadata.extend}"
                filepath = PathExtend(task.path_files, file_name)
                continue
            data.extend(request.file.byte_chunk)
            filepath.write_file(data, "wb")
        return file_pb2.StringResponse(code="200")'''

    async def delete_file(self):
        pass
        '''file_name = f"{request.name}.{request.extend}"
        task = await self.__repository.get(request.id_task)
        filepath = PathExtend(task.path_files, file_name)
        filepath.delete_file()
        return file_pb2.StringResponse(code="200")'''