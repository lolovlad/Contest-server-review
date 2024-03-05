from pydantic import BaseModel


class BaseTask(BaseModel):
    time_work: int
    size_raw: int
    type_input: int
    type_output: int

    number_shipments: int = 100


class PostTask(BaseTask):
    pass


class UpdateTask(BaseTask):
    id: int


class Settings(BaseTask):
    id: int
    name_file: list[str]