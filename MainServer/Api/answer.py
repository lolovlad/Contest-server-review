from fastapi import Depends, APIRouter, status, Response
from fastapi.responses import JSONResponse
from ..Services.AnswersServices import AnswersServices
from ..Models import SendAnswer, GetAnswer


router = APIRouter(prefix="/answer", tags=["answer"])


@router.post("/send_answer/{id_task}", responses={
    status.HTTP_200_OK: {"message": "answer cheking"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "error"},
    status.HTTP_404_NOT_FOUND: {"message": "task not found"}
})
async def send_answer(id_task: int,
                      send_answer_model: SendAnswer,
                      service: AnswersServices = Depends()):
    await service.send_answer(id_task,
                              send_answer_model.id_compilation,
                              send_answer_model.id_contest,
                              send_answer_model.id_user,
                              send_answer_model.program_file)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "answer cheking"}
    )


@router.get("/list_answer_task/{id_task}", response_model=list[GetAnswer], responses={
    status.HTTP_404_NOT_FOUND: {"message": "not finde"}
})
async def get_list_answers_task(id_task: int,
                                type_contest: str,
                                id_user: int,
                                service: AnswersServices = Depends()):
    list_answers = await service.get_list_answers_task(type_contest, id_task, id_user)
    return list_answers


@router.get("/list_answer_contest/{id_contest}",  response_model=list[GetAnswer], responses={
    status.HTTP_404_NOT_FOUND: {"message": "not finde"}
})
async def get_answers_contest(id_contest: int,
                              id_user: int,
                              service: AnswersServices = Depends()):
    list_answer = await service.get_answers_contest(id_contest, id_user)
    return list_answer


@router.get("/get_report_file/{id_answer}", responses={
    status.HTTP_200_OK: {"message": ""}
})
async def get_report_file(id_answer: int,
                          service: AnswersServices = Depends()):
    response = await service.get_report_file(id_answer)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": response}
    )

