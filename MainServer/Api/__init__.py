from fastapi import APIRouter
from .settings import router as router_settings
from .task_file_settings_test import router as router_task_file_settings_test
from .compiler import router as router_compiler
from .answer import router as router_answer
from .contest import router as router_contest
from .file import router as router_file

router = APIRouter(prefix="/v1")
router.include_router(router_settings)
router.include_router(router_task_file_settings_test)
router.include_router(router_compiler)
router.include_router(router_answer)
router.include_router(router_contest)
router.include_router(router_file)


