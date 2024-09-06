from ..redis import async_session as redis_session
from ..database import async_session as db_session

from ..Models.MessageRedis import ResultCheckMessage
from ..tables import Answer


class ReviewDockerServices:
    def __init__(self):
        self.__db_session = db_session
        self.__redis_session = redis_session

    async def get_message_in_redis(self) -> ResultCheckMessage:
        async with self.__redis_session.client() as c:
            message = await c.brpop(["container_message"])
            return ResultCheckMessage.model_validate_json(message[1])

    async def save_result_in_db(self, message: ResultCheckMessage):
        async with self.__db_session() as session:
            answer = await session.get(Answer, int(message.trace_uuid))

            answer.total = message.total
            answer.time = message.time
            answer.memory_size = message.memory_size
            answer.number_test = message.number_test
            answer.points = message.points

            answer.path_report_file = message.path_report_file
            answer.is_completed = True

            try:
                session.add(answer)
                await session.commit()
            except:
                await session.rollback()