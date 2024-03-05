from fastapi import Depends
from ..tables import TypeCompilation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_session

from typing import List


class TypeCompilationRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get_list(self) -> List[TypeCompilation]:
        request = select(TypeCompilation).where()
        result = await self.__session.execute(request)
        return result.scalars().all()

    async def get(self, id_compilation: int) -> TypeCompilation | None:
        return await self.__session.get(TypeCompilation, id_compilation)
