from .protos import file_pb2, file_pb2_grpc
from ..settings import settings
from Classes.PathExtend import PathExtend
from ..database import get_session
from ..tables import Task


class FileProtoService(file_pb2_grpc.FileApiServicer):
    async def UploadFile(self, request_iterator, context):
        session = get_session()

        data = bytearray()
        filepath = settings.static_path

        async for request in request_iterator:
            if request.metadata.name and request.metadata.extend:
                task = session.query(Task).filter(Task.id == request.metadata.id_task).first()
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
        session = get_session()
        file_name = f"{request.name}.{request.extend}"
        task = session.query(Task).filter(Task.id == request.metadata.id_task).first()
        filepath = PathExtend(task.path_files, file_name)
        filepath.delete_file()
        return file_pb2.StringResponse(code="200")
