from fastapi import Depends, APIRouter, status, UploadFile, Form, File, BackgroundTasks, Response
from fastapi.responses import JSONResponse
from ..Services.AnswersServices import AnswersServices
from ..Models import SendAnswer, GetAnswer, GetAnswerNew, AnswerReview, PutPointAnswer

from Classes.CheckAnswer.CheckingAnswers import check_answer


router = APIRouter(prefix="/answer", tags=["answer"])


@router.post("/send_answer/{id_task}", responses={
    status.HTTP_200_OK: {"message": "answer cheking"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "error"},
    status.HTTP_404_NOT_FOUND: {"message": "task not found"}
})
async def send_answer(id_task: int,
                      background_tasks: BackgroundTasks,
                      id_contest: int = Form(...),
                      type_task: str = Form(...),
                      id_compilation: int = Form(...),
                      id_user: int = Form(...),
                      file: UploadFile = File(...),
                      service: AnswersServices = Depends()):

    answer, task = await service.send_answer(id_task,
                                             id_compilation,
                                             id_user,
                                             file,
                                             id_contest,
                                             type_task)
    if type_task == "programming":
        background_tasks.add_task(check_answer, answer, task)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "answer cheking"}
    )


@router.get("/list_answer_task/{id_contest}/{id_task}", response_model=list[GetAnswer], responses={
    status.HTTP_404_NOT_FOUND: {"message": "not finde"}
})
async def get_list_answers_task(id_contest: int,
                                id_task: int,
                                type_contest: str,
                                id_user: int,
                                service: AnswersServices = Depends()):
    list_answers = await service.get_list_answers_task(id_contest, type_contest, id_task, id_user)
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


@router.get("/{id_contest}/{id_task}/{id_user}/list", response_model=list[GetAnswerNew], responses={
    status.HTTP_404_NOT_FOUND: {"message": "not finde"}
})
async def get_answer_page_list(response: Response,
                               id_contest: int,
                               id_task: int,
                               id_user: int,
                               page: int = 1,
                               answer_service: AnswersServices = Depends()):
    count_page = await answer_service.get_count_page_in_user(id_contest, id_task, id_user)
    response.headers["X-Count-Page"] = str(count_page)
    response.headers["X-Count-Item"] = str(answer_service.count_item)
    ans_list = await answer_service.get_list_answers_page(id_contest, id_task, id_user, page)
    return ans_list


@router.get("/review/{id_answer}", response_model=AnswerReview)
async def get_review_answer(id_answer: int,
                            answer_service: AnswersServices = Depends()):
    answer = await answer_service.get_review_answer(id_answer)
    return answer


@router.put("/review/point/{id_answer}")
async def update_point_answer(id_answer: int,
                              answer: PutPointAnswer,
                              answer_service: AnswersServices = Depends()):
    await answer_service.update_point_answer(id_answer, answer)
