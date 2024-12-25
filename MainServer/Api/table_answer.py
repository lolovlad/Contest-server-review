from fastapi import Depends, APIRouter, status, BackgroundTasks, Response
from fastapi.responses import JSONResponse

from ..Repositories.TableRepository import TableRepository


router = APIRouter(prefix="/table", tags=["table"])


@router.post("/{id_contest}/update", responses={
    status.HTTP_200_OK: {"message": "synchronized"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "error"},
    status.HTTP_404_NOT_FOUND: {"message": "error"}
})
async def update_table(id_contest: int,
                       table: dict,
                       repo: TableRepository = Depends()):
    await repo.save_table(id_contest, table)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "synchronized"}
    )


@router.get("/all/{id_contest}", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "error"},
    status.HTTP_404_NOT_FOUND: {"message": "error"}
})
async def get_all_table(id_contest: int,
                        repo: TableRepository = Depends()):
    table = await repo.get_table(id_contest)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"table": table}
    )


@router.get("/{id_contest}/{id_user}", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "error"},
    status.HTTP_404_NOT_FOUND: {"message": "error"}
})
async def get_row_user(id_contest: int,
                       id_user: int,
                       repo: TableRepository = Depends()):
    row = await repo.get_row_by_user(id_contest, id_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"row": row}
    )
