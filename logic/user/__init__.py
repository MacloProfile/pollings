from aiogram import Router


def get_user_router() -> Router:
    from . import start_command, main_servey, open_questions, back, number_servey, get_result_handlers

    router = Router()

    router.include_router(start_command.router)
    router.include_router(main_servey.router)
    router.include_router(open_questions.router)
    router.include_router(back.router)
    router.include_router(number_servey.router)
    router.include_router(get_result_handlers.router)

    return router
