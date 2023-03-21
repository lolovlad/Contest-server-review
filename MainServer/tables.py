from sqlalchemy import Column, Integer, String, LargeBinary, \
    DateTime, ForeignKey, Boolean, Text, Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
base = declarative_base()


class TypeCompilation(base):
    __tablename__ = "type_compilation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_compilation = Column(String, nullable=True)
    path_compilation = Column(String, nullable=True)
    path_commands = Column(String, nullable=True)
    extension = Column(String, nullable=False)


class Task(base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    time_work = Column(Integer, nullable=False)
    size_raw = Column(Integer, nullable=False)
    type_input = Column(Integer, nullable=False, default=1)
    type_output = Column(Integer, nullable=False, default=1)
    path_files = Column(String, nullable=False)

    number_shipments = Column(Integer, nullable=False, default=100)

    answers = relationship("Answer", backref="task", lazy=True, cascade="all, delete")


class Answer(base):
    __tablename__ = "answer"

    date_send = Column(DateTime, nullable=False, default=datetime.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_team = Column(Integer, default=0)
    id_user = Column(Integer)
    id_task = Column(Integer, ForeignKey('task.id'))
    id_contest = Column(Integer)
    type_compiler = Column(Integer, ForeignKey('type_compilation.id'), default=1)
    total = Column(String, nullable=False, default="-")
    time = Column(String, nullable=False, default="-")
    memory_size = Column(Float, nullable=False, default=0)
    number_test = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)

    path_report_file = Column(String, nullable=False, default="None")
    path_programme_file = Column(String, nullable=False)

    compilation = relationship('TypeCompilation', backref='type_compilation', lazy='joined')