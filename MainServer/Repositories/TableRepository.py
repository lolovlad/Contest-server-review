from ..tables import TableContest
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from ..database import get_session


class TableRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get_table_by_id(self, id_contest: int) -> TableContest | None:
        request = select(TableContest).where(TableContest.id_contest == id_contest)
        result = await self.__session.execute(request)
        return result.scalars().first()

    async def save_table(self, id_contest: int, table: dict):
        table_model = await self.get_table_by_id(id_contest)
        if table_model is None:
            self.__session.add(TableContest(id_contest=id_contest,
                                            table_result=table))
            await self.__session.commit()
        else:
            table_model.table_result = table
            flag_modified(table_model, "table_result")
            self.__session.add(table_model)
            await self.__session.commit()

    async def get_row_by_user(self, id_contest: int, id_user: int) -> dict:
        request = select(TableContest.table_result[str(id_user)]).where(TableContest.id_contest == id_contest)
        result = await self.__session.execute(request)
        return result.scalars().first()

    async def get_table(self, id_contest: int) -> dict:
        request = select(TableContest.table_result).where(TableContest.id_contest == id_contest)
        result = await self.__session.execute(request)
        return result.scalars().first()