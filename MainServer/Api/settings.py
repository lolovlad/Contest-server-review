from fastapi import Depends, APIRouter, status, Response
from fastapi.responses import JSONResponse
from ..Services.SettingsProtoServices import SettingsProtoServices
from ..Models import PostTask, Settings, UpdateTask


router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("/{id_task}", responses={
    status.HTTP_201_CREATED: {"message": "create"}
})
async def create_settings(id_task: int,
                          task: PostTask,
                          service: SettingsProtoServices = Depends()):
    await service.settings_post(id_task, task)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "create"}
    )


@router.get("/get_settings/{id_settings}", response_model=Settings,  responses={
    status.HTTP_404_NOT_FOUND: {"message": "null"}
})
async def get_settings(id_settings: int,
                       service: SettingsProtoServices = Depends()):
    settings = await service.settings_get(id_settings)
    return settings


@router.delete("/{id_task}", responses={
    status.HTTP_200_OK: {"message": "delete"}
})
async def delete_settings(id_task: int,
                          service: SettingsProtoServices = Depends()):
    await service.settings_delete(id_task)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "delete"}
    )


@router.put("/", responses={
    status.HTTP_205_RESET_CONTENT: {}
})
async def update_settings(task: UpdateTask,
                          service: SettingsProtoServices = Depends()):
    await service.settings_update(task)
    return JSONResponse(
        status_code=status.HTTP_205_RESET_CONTENT,
        content={}
    )
