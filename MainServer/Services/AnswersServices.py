from fastapi import Depends
from ..tables import TypeCompilation, Answer, Task

from Classes.PathExtend import PathExtend
from ..Models.TaskTestSettings import FileTaskTest
from ..Models import GetAnswer

from sqlalchemy import func


from json import load, dumps
from datetime import datetime

from ..Repositories import *

from Classes.CheckAnswer.CheckingAnswers import check_answer


class AnswersServices:
    def __init__(self,
                 repo_task: TaskRepository = Depends(),
                 repo_answer: AnswerRepository = Depends(),
                 repo_type_compilation: TypeCompilationRepository = Depends(),
                 repo_contest_report: ContestReportRepository = Depends()):
        self.__repo_task: TaskRepository = repo_task
        self.__repo_answer: AnswerRepository = repo_answer
        self.__repo_type_compil: TypeCompilationRepository = repo_type_compilation
        self.__repo_contest_report: ContestReportRepository = repo_contest_report

    async def __find_json_file(self, path: PathExtend):
        for name in path.list_file_in_folder():
            if name.endswith("json"):
                return PathExtend(path.abs_path(), name)
        return ""

    async def __get_model_json(self, id_task: int):
        task = await self.__repo_task.get(id_task)
        path = PathExtend(task.path_files)
        filename = await self.__find_json_file(path)
        with open(filename.abs_path(), "r") as file:
            file_json = FileTaskTest(**load(file))
        return path, file_json

    async def send_answer(self, id_task: int,
                          id_compilation: int,
                          id_contest: int,
                          id_user: int,
                          program_file: str):

        path_settings, file_json = await self.__get_model_json(id_task)

        compiler = await self.__repo_type_compil.get(id_compilation)

        name_file = PathExtend.create_file_name(compiler.extension)
        string_path_file = f"Answers/{id_contest}_{id_user}/{name_file}"
        path_file = PathExtend("Answers", f"{id_contest}_{id_user}", name_file)
        path_file.create_folder()
        path_file.write_file(program_file, "wb")

        answer = Answer(
            id_user=id_user,
            id_task=id_task,
            id_contest=id_contest,
            type_compiler=compiler.id,
            path_programme_file=string_path_file
        )

        answer = await self.__repo_answer.add(answer)

        async for response in check_answer(answer.id):
            pass

    async def get_list_answers_task(self,
                                    type_contest: str,
                                    id_task: int,
                                    id: int) -> list[GetAnswer]:
        answers = []
        if type_contest == "team":
            answers = await self.__repo_answer.get_list_by_id_task_and_team(id_task, id)

        elif type_contest == "solo":
            answers = await self.__repo_answer.get_list_by_id_task_and_user(id_task, id)

        proto_answers = []
        for answer in answers:
            date: datetime = answer.date_send
            proto_answers.append(GetAnswer(
                date_send=date.isoformat(),
                id=answer.id,
                id_team=answer.id_team,
                id_user=answer.id_user,
                id_task=answer.id_task,
                id_contest=answer.id_contest,
                name_compilation=answer.compilation.name_compilation,
                total=answer.total,
                time=answer.time,
                memory_size=str(answer.memory_size),
                number_test=answer.number_test,
                points=answer.points,
            ))
        return proto_answers

    async def get_answers_contest(self, id_contest: int, id: int) -> list[GetAnswer]:
        ans = await self.__repo_answer.get_by_id_contest(id_contest)
        if ans is not None:
            if ans.id_team == 0:
                answers = await self.__repo_contest_report.get_max_points_by_contest_and_user(id_contest, id)
            else:
                answers = await self.__repo_contest_report.get_max_points_by_contest_and_team(id_contest, ans.id_team)

        else:
            answers = []
        proto_answers = []
        for answer in answers:
            date: datetime = answer.date_send
            proto_answers.append(GetAnswer(
                date_send=date.isoformat(),
                id=answer.id,
                id_team=answer.id_team,
                id_user=answer.id_user,
                id_task=answer.id_task,
                id_contest=answer.id_contest,
                name_compilation=answer.compilation.name_compilation,
                total=answer.total,
                time=answer.time,
                memory_size=str(answer.memory_size),
                number_test=answer.number_test,
                points=answer.points,
            ))
        return proto_answers

    async def get_report_file(self, id_answer: int) -> str:
        answer = await self.__repo_answer.get(id_answer)
        file_report = answer.path_report_file
        with open(file_report, "r") as file:
            file_json = load(file)
        json_answer = dumps(file_json)
        return json_answer
