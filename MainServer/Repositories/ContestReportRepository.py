from fastapi import Depends
from ..tables import Answer, ContestReport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session

from typing import List


class ContestReportRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def add(self, contest_report: ContestReport):
        try:
            self.__session.add(contest_report)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def update(self, contest_report: ContestReport):
        try:
            self.__session.add(contest_report)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def get_by_contest_task_user(self, id_contest: int, id_task: int, id_user: int) -> ContestReport | None:
        request = select(ContestReport). \
            where(ContestReport.id_contest == id_contest). \
            where(ContestReport.id_task == id_task).\
            where(ContestReport.id_user == id_user)
        result = await self.__session.execute(request)
        return result.scalars().first()

    async def get_by_contest_task_team(self, id_contest: int, id_task: int, id_team: int) -> ContestReport | None:
        request = select(ContestReport). \
            where(ContestReport.id_contest == id_contest). \
            where(ContestReport.id_task == id_task). \
            where(ContestReport.id_team == id_team)
        result = await self.__session.execute(request)
        return result.scalars().first()

    async def get_max_points_by_contest_and_user(self, id_contest: int, id_user: int) -> List[Answer]:
        request = select(ContestReport).\
            where(ContestReport.id_contest == id_contest).\
            where(ContestReport.id_user == id_user)
        result = await self.__session.execute(request)
        return [i.answer for i in result.scalars().all()]

    async def get_max_points_by_contest_and_team(self, id_contest: int, id_team: int) -> List[Answer]:
        request = select(ContestReport).\
            where(ContestReport.id_contest == id_contest).\
            where(ContestReport.id_team == id_team)
        result = await self.__session.execute(request)
        return [i.answer for i in result.scalars().all()]

    async def get_max_points_by_contest(self, id_contest: int) -> List[Answer]:
        request = select(ContestReport).\
            where(ContestReport.id_contest == id_contest)
        result = await self.__session.execute(request)
        return [i.answer for i in result.scalars().all()]