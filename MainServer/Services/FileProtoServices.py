from .protos import file_pb2, file_pb2_grpc
from ..settings import settings
from Classes.PathExtend import PathExtend
from ..database import AsySession
from ..tables import Task
from ..Repositories import TaskRepository


class FileProtoService(file_pb2_grpc.FileApiServicer):
    async def UploadFile(self, request_iterator, context):
        data = bytearray()
        filepath = settings.static_path
        async with AsySession() as session:
            task_repo = TaskRepository(session)
            async for request in request_iterator:
                if request.metadata.name and request.metadata.extend:
                    task = await task_repo.get(request.metadata.id_task)
                    if request.metadata.extend == "json":
                        filepath = PathExtend(task.path_files)
                        filepath.delete_files_in_folder(f".{request.metadata.extend}")
                    file_name = f"{request.metadata.name}.{request.metadata.extend}"
                    filepath = PathExtend(task.path_files, file_name)
                    continue
                data.extend(request.file.byte_chunk)

            filepath.write_file(data, "wb")
        return file_pb2.StringResponse(code="200")

    async def DeleteFile(self, request, context):
        async with AsySession() as session:
            task_repo = TaskRepository(session)
            file_name = f"{request.name}.{request.extend}"
            task = await task_repo.get(request.metadata.id_task)
            filepath = PathExtend(task.path_files, file_name)
            filepath.delete_file()
            return file_pb2.StringResponse(code="200")
