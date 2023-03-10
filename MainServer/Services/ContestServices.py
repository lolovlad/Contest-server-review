from .protos import contest_pb2, contest_pb2_grpc
from ..database import get_session

from sqlalchemy import func
from ..tables import Answer

from json import dumps


class ContestServices(contest_pb2_grpc.ContestApiServicer):
    async def GetReportTotal(self, request, context):
        session = get_session()
        ans = session.query(Answer).filter(Answer.id_contest == request.id_contest).first()
        if ans.id_team == 0:
            answers = session.query(Answer, func.max(Answer.points))\
                .where(Answer.id_contest == request.id_contest).group_by(Answer.id_task, Answer.id_user).all()
        else:
            answers = session.query(Answer, func.max(Answer.points))\
                .where(Answer.id_contest == request.id_contest).group_by(Answer.id_task, Answer.id_team).all()

        result = {}
        for answer, points in answers:
            if answer.id_user not in result:
                result[answer.id_user] = {
                    "name": str(answer.id_user),
                    "total": {answer.id_task: points},
                    "sum_point": points,
                    "name_contest": "",
                    "type_contest": 1 if ans.id_team == 0 else 2,
                }
            else:
                result[answer.id_user]["total"][answer.id_task] = points
                result[answer.id_user]["sum_point"] += points
        return contest_pb2.GetReportTotalResponse(result=dumps(result).encode())