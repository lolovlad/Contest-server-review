import subprocess
import time
from subprocess import Popen
import asyncio
import shlex

from .InputData import InputData
from .OutputData import OutputData
from .Compiler import Compiler
from .VirtualEnvironment import VirtualEnvironment
from .Models.ReportTesting import ReportTesting
from .Models.ReportTesting import Rating


class StartFileProgram:
    def __init__(self, virtual: VirtualEnvironment, input_stream: InputData,
                 output_stream: OutputData, type_compilation: Compiler):
        self.__venv = virtual
        self.__input_stream = input_stream
        self.__output_stream = output_stream
        self.__process = None
        self.__compiler = type_compilation

    async def __create_sub_proces(self):
        self.__process = await asyncio.create_subprocess_exec(*shlex.split(self.__compiler.command),
                                                              stdin=asyncio.subprocess.PIPE,
                                                              stdout=asyncio.subprocess.PIPE,
                                                              stderr=asyncio.subprocess.PIPE,
                                                              cwd=self.__venv.path_virtual_environment
                                                              )

    async def start_process(self, input_in_process, time_out: int) -> ReportTesting:
        input_data = self.__input_stream.start_stream(input_in_process)
        await self.__create_sub_proces()
        report_testing = ReportTesting()
        try:
            task = asyncio.Task(self.__process.communicate(input=input_data))
            done, pending = await asyncio.wait([task], timeout=time_out)
            if pending:
                report_testing.errors = Rating.TIME_LIMIT_EXCEEDED
                return report_testing

            outs = await task
            report_testing.out = self.__output_stream.read_output(str(outs[0].decode()))

            if len(outs[1].decode().split("\n")) > 2:
                raise Exception

            mt_out = str(outs[1].decode()).replace("\n", "").split()

            memory, time_work = map(float, mt_out)

            report_testing.memory = round((int(memory) / 2**10), 3)
            report_testing.time = int(time_work * 1000)
            report_testing.errors = Rating.OK
            return report_testing
        except Exception:
            report_testing.errors = Rating.COMPILATION_ERROR
            return report_testing
