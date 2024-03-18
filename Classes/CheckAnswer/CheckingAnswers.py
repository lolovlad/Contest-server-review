import heapq
from json import dump, loads, load


from typing import List, Set


from MainServer.Models.TaskTestSettings import FileTaskTest, CheckType, TypeTest, ChunkTest
from MainServer.tables import Answer, ContestReport, Task

from .InputData import InputData
from .StartFileProgram import StartFileProgram
from .OutputData import OutputData
from .VirtualEnvironment import VirtualEnvironment
from .Compiler import Compiler
from .Grading import Grading

from .Models.Report import Report, TestReport
from .Models.ReportTesting import Rating

from ..PathExtend import PathExtend

from .Models.Settings import Settings

from MainServer.database import async_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from MainServer.Repositories import ContestReportRepository

import os
from pathlib import Path


class CheckingAnswer:
    def __init__(self, file_settings_task: FileTaskTest, settings: Settings):
        super().__init__()
        self.__settings: Settings = settings
        self.__test: FileTaskTest = file_settings_task
        self.__path: PathExtend = PathExtend(settings.path_file_test)
        self.__file_answer: PathExtend = PathExtend(settings.path_file_answer)
        self.__graf = {}
        self.__test_report = []
        self.__grading: Grading = Grading(settings.max_size_memory)
        self.__run_file_program: StartFileProgram = None
        self.__virtual_environment: VirtualEnvironment = None
        self.__GRADING: List[str] = ["OK", "CE", "WA", "PE", "TL", "ML", "OL", "RE", "PCF", "IL"]

    @property
    def test_report(self):
        return self.__test_report

    def __read_answer(self, name_file_with_answer: str) -> str:
        answer = open(PathExtend(self.__path.abs_path(), name_file_with_answer).abs_path(), "r").readlines()
        return "".join(answer)

    def is_start_test(self, chunk_test: ChunkTest, list_ok_test: Set[int]) -> bool:
        if chunk_test.type_test == TypeTest.MAIN:
            if len(list_ok_test) > 0 and sorted(list_ok_test)[0] == 0:
                if len(chunk_test.settings_test.necessary_test) > 0:
                    return set(chunk_test.settings_test.necessary_test).issubset(list_ok_test)
                else:
                    return True
            else:
                return False
        else:
            return True

    async def testing_programme(self):
        visited = [False] * len(self.__graf)
        list_ok_test = set()
        queue = []

        visited[0] = True
        queue.append(0)
        id_info_test_global = 1
        while queue:

            id_chunk_test = queue.pop(0)

            chunk = self.__test.setting_tests[id_chunk_test]

            start_testing = self.is_start_test(chunk, list_ok_test)

            if start_testing:
                self.__test_report[id_chunk_test].state_report = True
                os_name = "win"
                for id_info_test, info_test in enumerate(chunk.tests):
                    if os_name == "win":
                        information = await self.__run_file_program.start_process(
                            PathExtend(self.__path.abs_path(), info_test.filling_type_variable),
                            self.__settings.timeout
                        )
                    else:
                        information = await self.__run_file_program.start_process(
                            PathExtend(self.__path.abs_path(), info_test.filling_type_variable),
                            self.__settings.timeout
                        )

                    correct_answer = self.__read_answer(info_test.answer)
                    #print(information.out, correct_answer, "testing")
                    grading = self.__grading.grading(information.out == correct_answer, information.errors, information.memory)

                    self.__test_report[id_chunk_test].list_test_report.append(self.__GRADING[grading.value - 1])

                    if chunk.settings_test.check_type == CheckType.ONE:
                        if self.__test_report[id_chunk_test].list_test_report[-1] != "OK":
                            self.__test_report[id_chunk_test].state_report = False
                            self.__test_report[id_chunk_test].state_test = f"test {id_info_test_global}"
                            self.__test_report[id_chunk_test].time.append(information.time)
                            self.__test_report[id_chunk_test].number_test = id_info_test_global
                            self.__test_report[id_chunk_test].memory.append(information.memory)
                            break
                        else:
                            self.__test_report[id_chunk_test].point_sum += info_test.score
                            self.__test_report[id_chunk_test].number_test = id_info_test_global
                            self.__test_report[id_chunk_test].time.append(information.time)
                            self.__test_report[id_chunk_test].memory.append(information.memory)
                    id_info_test_global += 1

                if self.__test_report[id_chunk_test].state_report:
                    self.__test_report[id_chunk_test].state_test = "test sucesfull"
                    self.__test_report[id_chunk_test].number_test = id_info_test_global
                    list_ok_test.add(id_chunk_test)

            for neighbour in self.__graf[id_chunk_test]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    queue.append(neighbour)

    def __create_graf(self):
        self.__graf = {i: set() for i in range(len(self.__test.setting_tests))}
        for v in range(1, len(self.__test.setting_tests)):
            if len(self.__test.setting_tests[v].settings_test.necessary_test) == 0:
                self.__graf[0].add(v)
            for i in self.__test.setting_tests[v].settings_test.necessary_test:
                self.__graf[i].add(v)

    def __precompilation_procces(self) -> bool:
        self.__create_graf()
        self.__test_report = [TestReport() for _ in range(len(self.__graf))]
        self.__virtual_environment = VirtualEnvironment()
        self.__virtual_environment.create_virtual_folder()
        input_data = InputData(self.__virtual_environment.path_virtual_environment)
        input_data.creating_input_data(self.__settings.type_input)

        output_data = OutputData(self.__virtual_environment.path_virtual_environment)
        output_data.creating_output_data(self.__settings.type_output)

        self.__virtual_environment.move_answer_file_to_virtual_environment(self.__file_answer)

        compiler = Compiler(self.__settings.path_compiler)

        is_error = compiler.run_preprocess({"path_folder": self.__virtual_environment.path_virtual_environment,
                                            "path_file": self.__virtual_environment.path_file_answer,
                                            "name_file": "main.exe"})

        if not is_error:
            self.__run_file_program = StartFileProgram(self.__virtual_environment, input_data, output_data, compiler)
            return True
        else:
            return False

    async def create(self) -> bool:

        if self.__precompilation_procces():
            return True
        else:
            self.__test_report[0].list_test_report.append("PCF")
            self.__test_report[0].time.append(0)
            self.__test_report[0].memory.append(0)
            self.__test_report[0].state_test="error"
            return False

    def destruction(self):
        self.__virtual_environment.destruction_virtual_folder()


def create_report_to_answer(report):
    pass


def find_json_file(path: PathExtend):
    for name in path.list_file_in_folder():
        if name.endswith("json"):
            return PathExtend(path.abs_path(), name)
    return ""


def get_model_json(path: PathExtend):
    filename = find_json_file(path)
    with open(filename.abs_path(), "r") as file:
        file_json = FileTaskTest(**load(file))
    return path, file_json


async def check_answer(answer: Answer, task: Task):
    path_file_test = task.path_files

    dir_path_file = PathExtend(answer.path_programme_file).path_file()
    path, test = get_model_json(PathExtend(path_file_test))

    settings = Settings()
    settings.type_input = task.type_input
    settings.type_output = task.type_output
    settings.timeout = task.time_work
    settings.max_size_memory = int(task.size_raw)
    settings.path_compiler = answer.compilation.path_commands
    settings.path_file_test = path.abs_path()
    settings.path_file_answer = answer.path_programme_file

    checking_answer = CheckingAnswer(file_settings_task=test,
                                     settings=settings)

    is_create = await checking_answer.create()
    if is_create:
        await checking_answer.testing_programme()
    checking_answer.destruction()
    reports = Report()
    answer_json = checking_answer.test_report
    reports.list_report = answer_json

    path_file_report = f"{dir_path_file}/{PathExtend.create_file_name('json')}"

    with open(path_file_report, 'w') as outfile:
        dump(loads(reports.json()), outfile, indent=6)

    answer.path_report_file = path_file_report

    points = 0
    times = []
    memory = []
    answers = []

    for i in answer_json:
        points += i.point_sum
        answers += i.list_test_report
        times += i.time
        memory += i.memory

    answer.total = "OK"

    for i in answers:
        if i != "OK":
            answer.total = i

    answer.memory_size = round(sum(memory) / len(memory), 3)
    answer.points = points
    answer.number_test = answer_json[-1].number_test
    answer.time = f"{int(sum(times) / len(times))} ms"
    answer.is_completed = True
    await safe_answer(answer)
    await add_max_result(answer)
    return answer


async def safe_answer(answer: Answer):
    async with async_session() as session:
        try:
            session.add(answer)
            await session.commit()
        except:
            await session.rollback()


async def add_max_result(answer: Answer):
    async with async_session() as session:
        request = select(ContestReport). \
            where(ContestReport.id_task == answer.id_task). \
            where(ContestReport.id_user == answer.id_user).\
            where(ContestReport.id_contest == answer.id_contest)
        result = await session.execute(request)
        get_cur = result.scalars().first()

        if get_cur is not None:
            if answer.points > get_cur.answer.points:
                get_cur.id_answer = answer.id
                try:
                    session.add(get_cur)
                    await session.commit()
                except:
                    await session.rollback()
        else:
            get_cur = ContestReport(
                id_contest=answer.id_contest,
                id_task=answer.id_task,
                id_user=answer.id_user,
                id_team=0,
                id_answer=answer.id
            )
            try:
                session.add(get_cur)
                await session.commit()
            except:
                await session.rollback()