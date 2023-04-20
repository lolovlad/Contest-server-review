from .protos import contest_pb2, contest_pb2_grpc
from ..Repositories import AnswerRepository, ContestReportRepository

from sqlalchemy import func
from ..tables import Answer

from json import dumps


class ContestServices(contest_pb2_grpc.ContestApiServicer):

    def __init__(self):
        super().__init__()
        self.__repository: AnswerRepository = AnswerRepository()
        self.__repo_contest: ContestReportRepository = ContestReportRepository()

    async def GetReportTotal(self, request, context):
        ans = await self.__repository.get_by_id_contest(request.id_contest)
        answers = await self.__repo_contest.get_max_points_by_contest(request.id_contest)

        result = {}
        for answer in answers:
            if answer.id_user not in result:
                result[answer.id_user] = {
                    "name": str(answer.id_user),
                    "total": {answer.id_task: answer.points},
                    "sum_point": answer.points,
                    "name_contest": "",
                    "type_contest": 1 if ans.id_team == 0 else 2,
                }
            else:
                result[answer.id_user]["total"][answer.id_task] = answer.points
                result[answer.id_user]["sum_point"] += answer.points
        return contest_pb2.GetReportTotalResponse(result=dumps(result).encode())