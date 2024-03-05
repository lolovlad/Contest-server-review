from fastapi import Depends
from ..tables import TypeCompilation
from ..Models import GetCompiler
from ..Repositories import TypeCompilationRepository


class CompilerServices:

    def __init__(self, repo_type_compilation: TypeCompilationRepository = Depends()):
        self.__repository: TypeCompilationRepository = repo_type_compilation

    async def get_list_compiler(self) -> list[GetCompiler]:
        compilers = await self.__repository.get_list()
        proto_compilers = []
        for compiler in compilers:
            proto_compilers.append(GetCompiler(
                id=compiler.id,
                name=compiler.name_compilation,
                extend="all"
            ))
        return proto_compilers

    async def get_compiler(self, id_compilation: int) -> GetCompiler:

        compiler = await self.__repository.get(id_compilation)
        return GetCompiler(
            id=compiler.id,
            name=compiler.name_compilation,
            extend="all"
        )
