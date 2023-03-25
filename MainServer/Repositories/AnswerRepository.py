from ..tables import Answer, TypeCompilation
from MainServer.database import AsySession
from sqlalchemy import select

from typing import List


class AnswerRepository:
    def __init__(self, session):
        self.__session = session

    async def get(self, id_answer: int) -> Answer:
        answer_corun = await self.__session.execute(
            select(Answer, TypeCompilation).join(Answer.compilation).where(Answer.id == id_answer)
        )
        answer = answer_corun.scalars().first()
        return answer

