from ..tables import Task, Answer
from MainServer.database import AsySession
from sqlalchemy import select

from typing import List


class TaskRepository:

    def __init__(self, session):
        self.__session = session

    async def get(self, id_task: int) -> Answer:
        task_corun = await self.__session.execute(
            select(Task).where(Task.id == id_task)
        )
        task = task_corun.scalars().first()
        return task
