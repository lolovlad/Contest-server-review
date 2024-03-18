from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from ..Services.TaskFileSettingsTestService import TaskFileSettingsTestService
from ..Models import SettingsTest, ChunkTest, SettingsTestStr, ChunkTestReturn


router = APIRouter(prefix="/task_file_settings_test", tags=["task file settings test"])


@router.get("/all_settings_tests/{id_file}", response_model=list[SettingsTestStr])
async def get_all_settings_tests(id_file: int,
                                 service: TaskFileSettingsTestService = Depends()):
    response = await service.get_all_settings_tests(id_file)
    return response


@router.get("/chunk_test/{id_file}", response_model=ChunkTestReturn)
async def get_chunk_test(id_file: int,
                         type_test: str,
                         index: int,
                         service: TaskFileSettingsTestService = Depends()):
    response = await service.get_chunk_test(id_file, type_test, index)
    return response
