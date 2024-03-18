from pydantic import BaseModel


class GetCompiler(BaseModel):
    id: int
    name: str
    extend: str


class GetNewCompilation(BaseModel):
    id: int
    name_compilation: str
    extension: str
