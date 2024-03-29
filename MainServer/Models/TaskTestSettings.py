from pydantic import BaseModel
from enum import Enum

from typing import List


class TypeTest(str, Enum):
    TEST = "test"
    MAIN = "main"


class CheckType(str, Enum):
    ONE = "one mistake"
    ALL = "many mistake"


class SettingsTest(BaseModel):
    limitation_variable: List[str]
    necessary_test: List[int]
    check_type: CheckType


class Test(BaseModel):
    score: int
    filling_type_variable: str
    answer: str


class ChunkTest(BaseModel):
    type_test: TypeTest = None
    settings_test: SettingsTest
    tests: List[Test]


class FileTaskTest(BaseModel):
    setting_tests: List[ChunkTest]


class SettingsTestStr(BaseModel):
    limitation_variable: str
    necessary_test: str
    check_type: CheckType


class ChunkTestReturn(BaseModel):
    settings_test: SettingsTestStr
    tests: list[Test]