from .protos import answer_pb2, answer_pb2_grpc
from ..tables import TypeCompilation, Answer, Task

from Classes.PathExtend import PathExtend
from ..Models.TaskTestSettings import FileTaskTest

from sqlalchemy import func
from json import load, dumps
from datetime import datetime

from ..Repositories import *

from Classes.CheckAnswer.CheckingAnswers import check_answer


class AnswersServices(answer_pb2_grpc.AnswerApiServicer):

    def __init__(self):
        super().__init__()
        self.__repo_task: TaskRepository = TaskRepository()
        self.__repo_answer: AnswerRepository = AnswerRepository()
        self.__repo_type_compil: TypeCompilationRepository = TypeCompilationRepository()

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

    async def SendAnswer(self, request, context):

        path_settings, file_json = await self.__get_model_json(request.id_task)

        compiler = await self.__repo_type_compil.get(request.id_compiler)

        name_file = PathExtend.create_file_name(compiler.extension)
        string_path_file = f"Answers/{request.id_contest}_{request.id_user}/{name_file}"
        path_file = PathExtend("Answers", f"{request.id_contest}_{request.id_user}", name_file)
        path_file.create_folder()
        path_file.write_file(request.program_file, "wb")

        answer = Answer(
            id_team=request.id_team,
            id_user=request.id_user,
            id_task=request.id_task,
            id_contest=request.id_contest,
            type_compiler=request.id_compiler,
            path_programme_file=string_path_file
        )

        answer = await self.__repo_answer.add(answer)

        async for response in check_answer(answer.id):
            yield answer_pb2.SendAnswerCodeResponse(code="200")

    async def GetListAnswersTask(self, request, context):
        answers = []
        if request.type_contest == "team":
            answers = await self.__repo_answer.get_list_by_id_task_and_team(request.id_task, request.id)

        elif request.type_contest == "solo":
            answers = await self.__repo_answer.get_list_by_id_task_and_user(request.id_task, request.id)

        proto_answers = []
        for answer in answers:
            date: datetime = answer.date_send
            proto_answers.append(answer_pb2.Answer(
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
        return answer_pb2.GetListAnswersTaskResponse(answers=proto_answers)

    async def GetAnswersContest(self, request, context):
        ans = await self.__repo_answer.get_by_id_contest(request.id_contest)
        if ans is not None:
            if ans.id_team == 0:
                answers = await self.__repo_answer.get_list_max_point_in_user(request.id_contest, request.id)
            else:
                answers = await self.__repo_answer.get_list_max_point_in_team(request.id_contest, ans.id_team)

        else:
            answers = []
        proto_answers = []
        for answer, points in answers:
            date: datetime = answer.date_send
            proto_answers.append(answer_pb2.Answer(
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
                points=points,
            ))
        return answer_pb2.GetAnswersContestResponse(answers=proto_answers)

    async def GetReportFile(self, request, context):
        answer = await self.__repo_answer.get(request.id_answer)
        file_report = answer.path_report_file
        with open(file_report, "r") as file:
            file_json = load(file)
        json_answer = dumps(file_json)
        return answer_pb2.GetReportFileResponse(report_file=json_answer.encode())