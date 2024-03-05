from fastapi import Depends

from ..Repositories import AnswerRepository, ContestReportRepository
from json import dumps


class ContestServices:
    def __init__(self,
                 repo_answer: AnswerRepository = Depends(),
                 repo_contest: ContestReportRepository = Depends()):
        self.__repository: AnswerRepository = repo_answer
        self.__repo_contest: ContestReportRepository = repo_contest

    async def get_report_total(self, id_contest: int) -> str:
        ans = await self.__repository.get_by_id_contest(id_contest)
        answers = await self.__repo_contest.get_max_points_by_contest(id_contest)

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
        return dumps(result)