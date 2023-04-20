from ..tables import Answer, TypeCompilation
from sqlalchemy import select
from sqlalchemy import func
from ..database import get_session

from typing import List


class AnswerRepository:

    async def get(self, id_answer: int) -> Answer | None:
        async with get_session() as session:
            return await session.get(Answer, id_answer)

    async def get_by_id_contest(self, id_contest: int) -> Answer | None:
        async with get_session() as session:
            request = select(Answer).where(Answer.id_contest == id_contest)
            result = await session.execute(request)
            return result.scalar().first()

    async def get_max_points_group_team_by_id_contest(self, id_contest: int) -> list:
        async with get_session() as session:
            request = session.query(Answer, func.max(Answer.points))\
                .where(Answer.id_contest == id_contest).group_by(Answer.id_task, Answer.id_team).all()
            result = await session.execute(request)
            return result.scalar().all()

    async def get_max_points_group_user_by_id_contest(self, id_contest: int) -> list:
        async with get_session() as session:
            request = select(Answer, func.max(Answer.points))\
                .where(Answer.id_contest == id_contest).group_by(Answer.id_task, Answer.id_user).all()
            result = await session.execute(request)
            return result.scalar().all()

    async def add(self, answer: Answer) -> Answer | None:
        async with get_session() as session:
            try:
                session.add(answer)
                await session.commit()
                return answer
            except:
                await session.rollback()

    async def get_list_by_id_task_and_team(self, id_task: int, id_team: int) -> List[Answer]:
        async with get_session() as session:
            request = select(Answer).\
                where(Answer.id_team == id_team).\
                where(Answer.id_task == id_task)

            result = await session.execute(request)
            return result.scalar().all()

    async def get_list_by_id_task_and_user(self, id_task: int, id_user: int) -> List[Answer]:
        async with get_session() as session:
            request = select(Answer). \
                where(Answer.id_user == id_user). \
                where(Answer.id_task == id_task)

            result = await session.execute(request)
            return result.scalar().all()

    async def get_by_contest_and_user_id(self, id_contest: int, id_user: int) -> Answer:
        async with get_session() as session:
            request = select(Answer). \
                where(Answer.id_user == id_user). \
                where(Answer.id_contest == id_contest)

            result = await session.execute(request)
            return result.scalar().first()

    async def get_list_max_point_in_team(self, id_contest: int, id_team: int) -> list:
        async with get_session() as session:
            request = select(Answer, func.max(Answer.points)).\
                where(Answer.id_team == id_team). \
                where(Answer.id_contest == id_contest).\
                group_by(Answer.id_task)

            result = await session.execute(request)
            return result.scalar().all()

    async def get_list_max_point_in_user(self, id_contest: int, id_user: int) -> list:
        async with get_session() as session:
            request = select(Answer, func.max(Answer.points)).\
                where(Answer.id_user == id_user). \
                where(Answer.id_contest == id_contest).\
                group_by(Answer.id_task)

            result = await session.execute(request)
            return result.scalar().all()

    async def update(self, answer: Answer):
        async with get_session() as session:
            try:
                session.add(answer)
                await session.commit()
            except:
                await session.rollback()

