from ..CheckAnswer.InputStream import InputStream
from ..CheckAnswer.InputFileStream import InputFileStream
from ..PathExtend import PathExtend
from .Models.Settings import TypeInput


class InputData:
    def __init__(self, path):
        self.__file_data = InputFileStream(path)
        self.__input_data = InputStream(path)
        self.__input_stream = None

    def creating_input_data(self, type_data):
        if type_data == TypeInput.STREAM:
            self.__input_stream = self.__input_data
        elif type_data == TypeInput.FILE:
            self.__input_stream = self.__file_data

    def start_stream(self, input_data: PathExtend):
        with open(input_data.abs_path(), "r") as file:
            input_data = file.readlines()
        return self.__input_stream.start_stream(input_data)


