import threading
from json import dump, loads, load

from os import chdir, getcwd
from typing import List
import asyncio

from MainServer.Models.TaskTestSettings import FileTaskTest, CheckType
from MainServer.tables import Answer, Task, TypeCompilation
from MainServer.database import AsySession

from .InputData import InputData
from .StartFileProgram import StartFileProgram
from .OutputData import OutputData
from .VirtualEnvironment import VirtualEnvironment
from .Compiler import Compiler
from .Grading import Grading

from .Models.Report import Report, TestReport
from .Models.ReportTesting import Rating

from ..PathExtend import PathExtend

from sqlalchemy import select
from threading import Thread


class CheckingAnswer(Thread):
    def __init__(self, test: FileTaskTest,
                 type_input: int,
                 type_output: int,
                 timeout: int,
                 size: int,
                 path_compiler: str,
                 path: PathExtend,
                 file_answer: str):
        super().__init__()
        self.__test: FileTaskTest = test
        self.__type_input = type_input
        self.__type_output = type_output
        self.__timeout = timeout
        self.__path_compiler = path_compiler
        self.__path = path
        self.__file_answer = PathExtend(file_answer)
        self.__graf = {}
        self.__test_report = []
        self.__grading: Grading = Grading(size)
        self.__GRADING: List[str] = ["OK", "CE", "WA", "PE", "TL", "ML", "OL", "RE", "PCF", "IL"]

    @property
    def test_report(self):
        return self.__test_report

    def __testing_programme(self, start_node, test_report, program_file, path_test: PathExtend, is_error: bool):
        visited = [False] * len(self.__graf)
        list_ok_test = set()
        queue = []

        visited[start_node] = True
        queue.append(start_node)
        while queue:

            id_chunk_test = queue.pop(0)
            start_testing = True

            chunk = self.__test.setting_tests[id_chunk_test]

            if len(chunk.settings_test.necessary_test) > 0:
                start_testing = set(chunk.settings_test.necessary_test).issubset(list_ok_test)

            id_info_test_global = 1

            if start_testing:
                test_report[id_chunk_test].state_report = True
                for id_info_test, info_test in enumerate(chunk.tests):
                    information = program_file.start_process(
                        PathExtend(path_test.abs_path(), info_test.filling_type_variable),
                        self.__timeout
                    )
                    if is_error:
                        information.errors = Rating.COMPILATION_ERROR

                    answer = open(PathExtend(path_test.abs_path(), info_test.answer).abs_path(), "r").readlines()
                    answer = "".join(answer)

                    grading = self.__grading.grading(information.out == answer, information.errors,
                                                         information.time, information.memory)

                    test_report[id_chunk_test].list_test_report.append(self.__GRADING[grading.value - 1])

                    if chunk.settings_test.check_type == CheckType.ONE:
                        if test_report[id_chunk_test].list_test_report[-1] != "OK":
                            test_report[id_chunk_test].state_report = False
                            test_report[id_chunk_test].state_test = f"test {id_info_test_global}"
                            test_report[id_chunk_test].time += [int(information.time)]
                            test_report[id_chunk_test].number_test = id_info_test_global
                            test_report[id_chunk_test].memory += information.memory
                            break
                        else:
                            test_report[id_chunk_test].point_sum += info_test.score
                            test_report[id_chunk_test].number_test = id_info_test_global
                            test_report[id_chunk_test].time += [int(information.time)]
                            test_report[id_chunk_test].memory += information.memory
                    id_info_test_global += 1

                if test_report[id_chunk_test].state_report:
                    test_report[id_chunk_test].state_test = "test sucesfull"
                    test_report[id_chunk_test].number_test = id_info_test_global
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

    def run(self):
        self.__create_graf()
        self.__test_report = [TestReport() for _ in range(len(self.__graf))]
        virtual_environment = VirtualEnvironment()
        virtual_environment.create_virtual_folder()
        input_data = InputData(virtual_environment.path_virtual_environment)
        input_data.creating_input_data(self.__type_input)

        output_data = OutputData(virtual_environment.path_virtual_environment)
        output_data.creating_output_data(self.__type_output)

        virtual_environment.move_answer_file_to_virtual_environment(self.__file_answer)

        compiler = Compiler(self.__path_compiler)

        is_error = compiler.run_preprocess({"path_folder": virtual_environment.path_virtual_environment,
                                            "path_file": virtual_environment.path_file_answer,
                                            "name_file": "main.exe"})

        program_file = StartFileProgram(virtual_environment, input_data, output_data, compiler)

        self.__testing_programme(0, self.__test_report, program_file, self.__path, is_error)

        virtual_environment.destruction_virtual_folder()


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


async def check_answer(answer_id: int):
    async with AsySession() as session:
        answer_corun = await session.execute(select(Answer, TypeCompilation).join(Answer.compilation).where(Answer.id == answer_id))
        answer = answer_corun.first()[0]

        task_corun = await session.execute(select(Task).where(Task.id == answer.id_task))

        task = task_corun.first()[0]

        path_file_test = task.path_files

        yield True

        dir_path_file = PathExtend(answer.path_programme_file).path_file()

        type_input = task.type_input
        type_output = task.type_output
        timeout = task.time_work
        size = task.size_raw
        path, test = get_model_json(PathExtend(path_file_test))

        checking_answer = CheckingAnswer(test,
                                         type_input,
                                         type_output,
                                         timeout,
                                         size,
                                         answer.compilation.path_commands,
                                         path,
                                         answer.path_programme_file)

        yield True
        checking_answer.start()
        #answer_json = await checking_answer.start_examination(path)
        while True:
            if checking_answer.is_alive():
                yield True
                await asyncio.sleep(1)
            else:
                break
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

        yield True

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
        await session.commit()
        yield False