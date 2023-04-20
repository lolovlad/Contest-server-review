from ..tables import Task, Answer
from sqlalchemy import select
from ..database import get_session


class TaskRepository:
    async def get(self, id_task: int) -> Task | None:
        async with get_session() as session:
            return await session.get(Task, id_task)

    async def add(self, task: Task):
        async with get_session() as session:
            try:
                session.add(task)
                await session.commit()
            except:
                await session.rollback()

    async def delete(self, task: Task):
        async with get_session() as session:
            try:
                await session.delete(task)
                await session.commit()
            except:
                await session.rollback()

    async def update(self, task) -> Task:
        async with get_session() as session:
            try:
                session.add(task)
                await session.commit()
                return task
            except:
                await session.rollback()