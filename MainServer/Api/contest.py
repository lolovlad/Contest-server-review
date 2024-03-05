from fastapi import Depends, APIRouter, status, Response
from fastapi.responses import JSONResponse
from ..Services.ContestServices import ContestServices
from ..Models import *


router = APIRouter(prefix="/contest", tags=["contest"])


@router.get("/get_report/{id_contest}", responses={
    status.HTTP_200_OK: {"message": ""}
})
async def get_report_total(id_contest: int,
                           service: ContestServices = Depends()):
    response = await service.get_report_total(id_contest)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": response}
    )