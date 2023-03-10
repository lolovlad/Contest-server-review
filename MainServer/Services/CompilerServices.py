from .protos import compiler_pb2, compiler_pb2_grpc
from ..database import get_session
from ..tables import TypeCompilation

from sqlalchemy.orm.session import Session


class CompilerServices(compiler_pb2_grpc.CompilerApiServicer):
    async def GetListCompiler(self, request, context):
        session = get_session()
        compilers = session.query(TypeCompilation).all()
        proto_compilers = []
        for compiler in compilers:
            proto_compilers.append(compiler_pb2.Compiler(
                id=compiler.id,
                name=compiler.name_compilation,
                extend="all"
            ))
        session.close()
        return compiler_pb2.GetListCompilerResponse(
            compilers=proto_compilers
        )

    async def GetCompiler(self, request, context):
        with self.__session() as session:
            compiler = session.query(TypeCompilation).filter(TypeCompilation.id == request.id).first()
        return compiler_pb2.Compiler(
            id=compiler.id,
            name=compiler.name_compilation,
            extend="all"
        )