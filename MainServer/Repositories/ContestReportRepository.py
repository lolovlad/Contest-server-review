from ..tables import Answer, ContestReport
from sqlalchemy import select
from sqlalchemy import func
from ..database import get_session

from typing import List


class ContestReportRepository:

    async def add(self, contest_report: ContestReport):
        async with get_session() as session:
            try:
                session.add(contest_report)
                await session.commit()
            except:
                await session.rollback()

    async def update(self, contest_report: ContestReport):
        async with get_session() as session:
            try:
                session.add(contest_report)
                await session.commit()
            except:
                await session.rollback()

    async def get_by_contest_and_task(self, id_contest: int, id_task: int) -> ContestReport | None:
        async with get_session() as session:
            request = select(ContestReport). \
                where(ContestReport.id_contest == id_contest). \
                where(ContestReport.id_task == id_task)
            result = await session.execute(request)
            return result.scalars().first()


    async def get_max_points_by_contest_and_user(self, id_contest: int, id_user: int) -> List[Answer]:
        async with get_session() as session:
            request = select(ContestReport).\
                where(ContestReport.id_contest == id_contest).\
                where(ContestReport.id_user == id_user)
            result = await session.execute(request)
            return [i.answer for i in result.scalars().all()]

    async def get_max_points_by_contest_and_team(self, id_contest: int, id_team: int) -> List[Answer]:
        async with get_session() as session:
            request = select(ContestReport).\
                where(ContestReport.id_contest == id_contest).\
                where(ContestReport.id_team == id_team)
            result = await session.execute(request)
            return [i.answer for i in result.scalars().all()]

    async def get_max_points_by_contest(self, id_contest: int) -> List[Answer]:
        async with get_session() as session:
            request = select(ContestReport).\
                where(ContestReport.id_contest == id_contest)
            result = await session.execute(request)
            return [i.answer for i in result.scalars().all()]