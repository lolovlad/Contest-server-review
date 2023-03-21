from .protos import answer_pb2, answer_pb2_grpc
from ..database import get_session
from ..tables import TypeCompilation, Answer, Task

from Classes.PathExtend import PathExtend
from ..Models.TaskTestSettings import FileTaskTest

from sqlalchemy.orm.session import Session
from sqlalchemy import func
from json import load, dumps
from datetime import datetime

from Classes.CheckAnswer.CheckingAnswers import check_answer


class AnswersServices(answer_pb2_grpc.AnswerApiServicer):
    async def __find_json_file(self, path: PathExtend):
        for name in path.list_file_in_folder():
            if name.endswith("json"):
                return PathExtend(path.abs_path(), name)
        return ""

    async def __get_model_json(self, id_task: int):
        session = get_session()
        task = session.query(Task).filter(Task.id == id_task).first()
        path = PathExtend(task.path_files)
        filename = await self.__find_json_file(path)
        with open(filename.abs_path(), "r") as file:
            file_json = FileTaskTest(**load(file))
        session.close()
        return path, file_json

    async def SendAnswer(self, request, context):
        session = get_session()

        path_settings, file_json = await self.__get_model_json(request.id_task)

        compiler = session.query(TypeCompilation).filter(TypeCompilation.id == request.id_compiler).first()

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

        session.add(answer)
        session.commit()
        async for response in check_answer(answer.id):
            print(response, "programme")
            yield answer_pb2.SendAnswerCodeResponse(code="200")
        session.close()

    async def GetListAnswersTask(self, request, context):
        session = get_session()
        answers = []
        if request.type_contest == "team":
            answers = session.query(Answer).\
                filter(Answer.id_team == request.id).\
                filter(Answer.id_task == request.id_task).all()
        elif request.type_contest == "solo":
            answers = session.query(Answer).\
                filter(Answer.id_user == request.id).\
                filter(Answer.id_task == request.id_task).all()

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
        session.close()
        return answer_pb2.GetListAnswersTaskResponse(answers=proto_answers)

    async def GetAnswersContest(self, request, context):
        session = get_session()
        ans = session.query(Answer).\
            filter(Answer.id_contest == request.id_contest).\
            filter(Answer.id_user == request.id).first()
        if ans is not None:
            if ans.id_team == 0:
                answers = session.query(Answer, func.max(Answer.points)) \
                    .where(Answer.id_contest == request.id_contest).where(Answer.id_user == request.id).group_by(Answer.id_task).all()
            else:
                answers = session.query(Answer, func.max(Answer.points)) \
                    .where(Answer.id_contest == request.id_contest).where(Answer.id_team == ans.id_team).group_by(Answer.id_task).all()
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
        session.close()
        return answer_pb2.GetAnswersContestResponse(answers=proto_answers)

    async def GetReportFile(self, request, context):
        session = get_session()
        answer = session.query(Answer).filter(Answer.id == request.id_answer).first()
        file_report = answer.path_report_file
        with open(file_report, "r") as file:
            file_json = load(file)
        json_answer = dumps(file_json)
        return answer_pb2.GetReportFileResponse(report_file=json_answer.encode())