from pydantic import BaseModel
from .AnswerSettings import AnswerSettings


class StartCheckMessage(BaseModel):
    id_trase: str
    lang: str
    path_file_test: str
    path_file_answer: str
    settings: AnswerSettings


class ResultCheckMessage(BaseModel):
    trace_uuid: str
    total: str = None
    memory_size: float = None
    points: int = None
    number_test: int = None
    time: str = None
    path_report_file: str = None
