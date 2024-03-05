from pydantic import BaseModel


class GetCompiler(BaseModel):
    id: int
    name: str
    extend: str

