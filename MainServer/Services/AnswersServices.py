from fastapi import Depends, UploadFile
from ..tables import TypeCompilation, Answer, Task, ContestReport

from Classes.PathExtend import PathExtend
from ..Models.TaskTestSettings import FileTaskTest
from ..Models import GetAnswer, GetAnswerNew, AnswerReview, PutPointAnswer

from sqlalchemy import func


from json import load, dumps
from datetime import datetime
from aiofiles import open as open_aio

from ..Repositories import *


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
        self.__count_item: int = 20

    @property
    def count_item(self) -> int:
        return self.__count_item

    async def get_count_page(self) -> int:
        count_row = await self.__repo_answer.count_row()
        i = int(count_row % self.__count_item != 0)
        return count_row // self.__count_item + i

    async def get_count_page_in_user(self,
                                     id_contest: int,
                                     id_task: int,
                                     id_user: int) -> int:
        count_row = await self.__repo_answer.count_row_user(id_contest,
                                                            id_task,
                                                            id_user)
        i = int(count_row % self.__count_item != 0)
        return count_row // self.__count_item + i

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
                          id_user: int,
                          program_file: UploadFile,
                          id_contest: int,
                          type_task: str):

        if type_task == "programming":
            path_settings, file_json = await self.__get_model_json(id_task)
            compiler = await self.__repo_type_compil.get(id_compilation)
            name_file = PathExtend.create_file_name(compiler.extension)
        else:
            name_file = PathExtend.create_file_name(".txt")
        string_path_file = f"Answers/{id_task}_{id_user}/{name_file}"
        path_file = PathExtend("Answers", f"{id_task}_{id_user}", name_file)
        path_file.create_folder()

        async with open_aio(str(path_file), 'wb') as out_file:
            while content := await program_file.read(1024):
                await out_file.write(content)
        if type_task == "programming":
            answer = Answer(
                id_user=id_user,
                id_task=id_task,
                id_contest=id_contest,
                type_compiler=compiler.id,
                path_programme_file=string_path_file
            )
        else:
            answer = Answer(
                id_user=id_user,
                id_task=id_task,
                id_contest=id_contest,
                path_programme_file=string_path_file,
                total="OK",
                time="0",
                memory_size=0,
                number_test=1,
                is_completed=False
            )

        answer = await self.__repo_answer.add(answer)

        task = await self.__repo_task.get(id_task)

        return answer, task

    async def get_list_answers_task(self,
                                    id_contest: int,
                                    type_contest: str,
                                    id_task: int,
                                    id_user: int) -> list[GetAnswer]:
        answers = []
        if type_contest == "team":
            answers = await self.__repo_answer.get_list_by_id_task_and_team(id_task, id_user)

        elif type_contest == "solo":
            answers = await self.__repo_answer.get_list_by_id_task_and_user(id_contest, id_task, id_user)

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

    async def get_list_answers_page(self,
                                    id_contest: int,
                                    id_task: int,
                                    id_user: int,
                                    number_page: int) -> list[GetAnswerNew]:
        offset = (number_page - 1) * self.__count_item
        answers_list_entity = await self.__repo_answer.get_page_answer(offset,
                                                                       self.__count_item,
                                                                       id_contest,
                                                                       id_task,
                                                                       id_user)
        answers_reg = [GetAnswerNew.model_validate(i, from_attributes=True) for i in answers_list_entity]
        return answers_reg

    async def get_review_answer(self, id_answer: int) -> AnswerReview:
        answer = await self.__repo_answer.get(id_answer)

        file = PathExtend(answer.path_programme_file)

        review = AnswerReview.model_validate(answer, from_attributes=True)
        review.file_answer = file.read_file()

        return review

    async def update_point_answer(self, id_answer: int, answer_data: PutPointAnswer):
        answer = await self.__repo_answer.get(id_answer)
        answer.points = answer_data.points
        await self.__repo_answer.update(answer)

        get_cur = await self.__repo_contest_report.get_by_contest_task_user(
            answer.id_contest,
            answer.id_task,
            answer.id_user
        )
        if get_cur is not None:
            if answer.points > get_cur.answer.points:
                get_cur.id_answer = answer.id
                await self.__repo_contest_report.update(get_cur)
        else:
            get_cur = ContestReport(
                id_contest=answer.id_contest,
                id_task=answer.id_task,
                id_user=answer.id_user,
                id_team=0,
                id_answer=answer.id
            )
            await self.__repo_contest_report.add(get_cur)