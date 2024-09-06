from fastapi import APIRouter, Depends, UploadFile
from ..Services.FileServices import FileServices


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload_file/{id_task}")
async def upload_files(id_task: int,
                       file: UploadFile,
                       file_service: FileServices = Depends()):
    await file_service.upload_file_s3(id_task, file)
    return {"filenames": file.filename}


@router.post("/upload_json_file/{id_task}")
async def upload_json_files(id_task: int,
                            file: UploadFile,
                            file_service: FileServices = Depends()):
    await file_service.upload_file_s3(id_task, file)
    return {"filenames": file.filename}


@router.delete("/delete_file/{id_task}/{filename}")
async def delete_file(id_task: int,
                      filename: str,
                      file_service: FileServices = Depends()):
    await file_service.delete_file(id_task, filename)
    return {"filenames": filename}