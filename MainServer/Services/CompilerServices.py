from .protos import compiler_pb2, compiler_pb2_grpc
from ..tables import TypeCompilation
from ..Repositories import TypeCompilationRepository


class CompilerServices(compiler_pb2_grpc.CompilerApiServicer):

    def __init__(self):
        super().__init__()
        self.__repository: TypeCompilationRepository = TypeCompilationRepository()

    async def GetListCompiler(self, request, context):
        compilers = await self.__repository.get_list()
        proto_compilers = []
        for compiler in compilers:
            proto_compilers.append(compiler_pb2.Compiler(
                id=compiler.id,
                name=compiler.name_compilation,
                extend="all"
            ))
        return compiler_pb2.GetListCompilerResponse(
            compilers=proto_compilers
        )

    async def GetCompiler(self, request, context):

        compiler = self.__repository.get()
        return compiler_pb2.Compiler(
            id=compiler.id,
            name=compiler.name_compilation,
            extend="all"
        )
