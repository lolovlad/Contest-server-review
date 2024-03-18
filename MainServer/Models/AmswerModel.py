from pydantic import BaseModel
from datetime import datetime
from .CompilerModel import GetNewCompilation


class GetAnswer(BaseModel):
    id: int
    date_send: str
    id_team: int = None
    id_user: int
    id_task: int
    id_contest: int
    name_compilation: str
    total: str
    time: str
    memory_size: str
    number_test: int
    points: int


class SendAnswer(BaseModel):
    id_compilation: int
    id_user: int
    program_file: str


class GetAnswerNew(BaseModel):
    date_send: datetime
    id: int
    id_team: int
    id_user: int
    id_task: int
    id_contest: int
    compilation: GetNewCompilation
    total: str
    time: str
    memory_size: float
    number_test: int
    points: int


class AnswerReview(BaseModel):
    date_send: datetime
    id: int
    compilation: GetNewCompilation
    total: str
    time: str
    memory_size: float
    number_test: int
    points: int
    file_answer: str = ""


class PutPointAnswer(BaseModel):
    points: int
