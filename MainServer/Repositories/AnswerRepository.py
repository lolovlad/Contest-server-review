from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..tables import Answer
from sqlalchemy import select
from ..database import get_session

from typing import List


class AnswerRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get(self, id_answer: int) -> Answer | None:
        return await self.__session.get(Answer, id_answer)

    async def get_by_id_contest(self, id_contest: int) -> Answer | None:
        request = select(Answer).where(Answer.id_contest == id_contest)
        result = await self.__session.execute(request)
        return result.scalars().first()

    async def add(self, answer: Answer) -> Answer | None:
        try:
            self.__session.add(answer)
            await self.__session.commit()
            return answer
        except:
            await self.__session.rollback()

    async def get_list_by_id_task_and_team(self, id_task: int, id_team: int) -> List[Answer]:
        request = select(Answer).\
            where(Answer.id_team == id_team).\
            where(Answer.id_task == id_task)

        result = await self.__session.execute(request)
        return result.scalars().all()

    async def get_list_by_id_task_and_user(self, id_task: int, id_user: int) -> List[Answer]:
        request = select(Answer). \
            where(Answer.id_user == id_user). \
            where(Answer.id_task == id_task)

        result = await self.__session.execute(request)
        return result.scalars().all()

    async def get_by_contest_and_user_id(self, id_contest: int, id_user: int) -> Answer:
        request = select(Answer). \
            where(Answer.id_user == id_user). \
            where(Answer.id_contest == id_contest)

        result = await self.__session.execute(request)
        return result.scalars().first()

    async def update(self, answer: Answer):
        try:
            self.__session.add(answer)
            await self.__session.commit()
        except:
            await self.__session.rollback()

