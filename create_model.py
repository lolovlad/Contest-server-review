from MainServer.tables import TypeCompilation
from MainServer.database import async_session
from asyncio import run
from uuid import uuid4


async def create_compilation_context():
    async with async_session() as session:
        compilations = [
            TypeCompilation(
                name_compilation="python",
                path_compilation="Commands/Python.txt",
                path_commands="Commands/Python.txt",
                extension="py"
            ),
            TypeCompilation(
                name_compilation="C++ 14",
                path_compilation="Commands/C++.txt",
                path_commands="Commands/C++.txt",
                extension="cpp"
            ),
            #TypeCompilation(
            #    name_compilation="txt",
            #    path_compilation="no command",
            #    path_commands="no command",
            #    extension="txt"
            #)
        ]

        session.add_all(compilations)

        await session.commit()


async def main():
    await create_compilation_context()


run(main())