from fastapi import Depends, APIRouter, status, Response
from fastapi.responses import JSONResponse
from ..Services.CompilerServices import CompilerServices
from ..Models import GetCompiler


router = APIRouter(prefix="/compiler", tags=["compiler"])


@router.get("/list", response_model=list[GetCompiler])
async def get_list_compiler(service: CompilerServices = Depends()):
    list_compiler = await service.get_list_compiler()
    return list_compiler


@router.get("/one/{id_compiler}", response_model=GetCompiler)
async def get_compiler(id_compilation: int,
                       service: CompilerServices = Depends()):
    compiler = await service.get_compiler(id_compilation)
    return compiler

