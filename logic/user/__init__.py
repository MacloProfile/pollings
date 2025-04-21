from aiogram import Router


def get_user_router() -> Router:
    from . import start_command, main_servey, open_questions, back, number_servey

    router = Router()
    router.include_router(start_command.router)
    router.include_router(main_servey.router)
    router.include_router(open_questions.router)
    router.include_router(back.router)
    router.include_router(number_servey.router)

    return router
