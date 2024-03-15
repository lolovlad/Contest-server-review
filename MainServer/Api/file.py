from fastapi import APIRouter, Depends, UploadFile
from ..Services.FileServices import FileServices


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload_file/{id_task}")
async def upload_files(id_task: int,
                       file: UploadFile,
                       file_service: FileServices = Depends()):
    await file_service.upload_file(id_task, file)
    return {"filenames": file.filename}


@router.post("/upload_json_file/{id_task}")
async def upload_json_files(id_task: int,
                            file: UploadFile,
                            file_service: FileServices = Depends()):
    await file_service.upload_file(id_task, file)
    return {"filenames": file.filename}


@router.delete("/delete_file/{id_task}/{filename}")
async def delete_file(id_task: int,
                      filename: str,
                      file_service: FileServices = Depends()):
    await file_service.delete_file(id_task, filename)
    return {"filenames": filename}


@router.delete("/delete_folder/{id_test}")
async def delete_folder(id_task: int,
                        file_service: FileServices = Depends()):
    file_service.delete_folder(id_task)
    return {}