from pydantic import BaseModel
from enum import Enum


class TypeInput(int, Enum):
    STREAM = 1
    FILE = 2


class TypeOutput(int, Enum):
    STREAM = 1
    FILE = 2


class CheckAnswer(BaseModel):
    time_work: int
    size_raw: int
    type_input: TypeInput
    type_output: TypeOutput
    file: bytes = b""
    id_compilation: int
    extension_file: str
