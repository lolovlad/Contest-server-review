from fastapi import UploadFile, Depends
from typing import List
from Classes.PathExtend import PathExtend

from ..database import get_session
from sqlalchemy.orm.session import Session

import shutil


class FileServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.__session = session

    def upload_file(self, id_task: int, file: UploadFile) -> None:
        file_name = PathExtend(f"Task_Id_{id_task}", "test", file.filename)
        file_name.create_folder()

        file_name.write_file_byte(file.file)

    def delete_file(self, id_task: int, name_file: str) -> None:
        file_name = PathExtend(f"Task_Id_{id_task}", "test", name_file)
        file_name.delete_file()

    def upload_json_file(self, id_task: int, file: UploadFile) -> None:
        name_json = PathExtend.create_file_name("json", start_name_file=f"task_test_{id_task}")

        path_json = PathExtend(f"Task_Id_{id_task}", name_json)
        path_json.write_file_byte(file.file)

    def delete_folder(self, id_task: int):
        folder_name = PathExtend(f"Task_Id_{id_task}")
        folder_name.delete_dir()