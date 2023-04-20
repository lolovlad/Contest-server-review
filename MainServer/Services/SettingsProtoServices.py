from .protos import settings_pb2, settings_pb2_grpc
from Classes.PathExtend import PathExtend
from ..database import get_session
from ..tables import Task
from ..Repositories import TaskRepository


class SettingsProtoServices(settings_pb2_grpc.SettingsApiServicer):

    def __init__(self):
        super().__init__()
        self.__repository: TaskRepository = TaskRepository()

    async def SettingsPost(self, request, context):
        name_folder = PathExtend.create_folder_name(10)
        folder = PathExtend(name_folder)
        folder.create_folder()

        task = Task(id=request.id,
                    time_work=request.time_work,
                    size_raw=request.size_raw,
                    type_input=request.type_input,
                    number_shipments=request.number_shipments,
                    path_files=name_folder)

        await self.__repository.add(task)
        return settings_pb2.CodeResponse(code="200")

    async def SettingsGet(self, request, context):

        task = await self.__repository.get(request.id)

        list_files = PathExtend(task.path_files).list_file_in_folder()

        settings = settings_pb2.Settings(id=task.id,
                                         time_work=task.time_work,
                                         size_raw=task.size_raw,
                                         type_input=task.type_input,
                                         type_output=task.type_output,
                                         number_shipments=task.number_shipments,
                                         name_file=list_files)
        return settings_pb2.GetSettingsResponse(settings=settings)

    async def SettingsDelete(self, request, context):
        task: Task = await self.__repository.get(request.id)
        path = PathExtend(task.path_files)
        path.delete_dir()
        await self.__repository.delete(task)
        return settings_pb2.CodeResponse(code="200")

    async def SettingsUpdate(self, request, context):

        task: Task = await self.__repository.get(request.id)
        task.size_raw = request.size_raw
        task.type_input = request.type_input
        task.type_output = request.type_output
        task.number_shipments = request.number_shipments
        task.time_work = request.time_work
        await self.__repository.update(task)
        return settings_pb2.CodeResponse(code="200")