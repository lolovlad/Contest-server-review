from fastapi import Depends
from ..tables import Task
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session


class TaskRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get(self, id_task: int) -> Task | None:
        return await self.__session.get(Task, id_task)

    async def add(self, task: Task):
        try:
            self.__session.add(task)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def delete(self, task: Task):
        try:
            await self.__session.delete(task)
            await self.__session.commit()
        except:
            await self.__session.rollback()

    async def update(self, task) -> Task:
        try:
            self.__session.add(task)
            await self.__session.commit()
            return task
        except:
            await self.__session.rollback()