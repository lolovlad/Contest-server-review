from pydantic import BaseModel


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
    id_contest: int
    id_user: int
    program_file: str

