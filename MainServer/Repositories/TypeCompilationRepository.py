from ..tables import TypeCompilation
from sqlalchemy import select
from ..database import get_session

from typing import List


class TypeCompilationRepository:
    async def get_list(self) -> List[TypeCompilation]:
        async with get_session() as session:
            request = select(TypeCompilation).where()
            result = await session.execute(request)
            return result.scalars().all()

    async def get(self, id_compilation: int) -> TypeCompilation | None:
        async with get_session() as session:
            return await session.get(TypeCompilation, id_compilation)
