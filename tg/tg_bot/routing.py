from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import User

base_router: Router = Router()

routers: tuple[Router, ...] = (base_router,)


@base_router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    user_attrs: tuple[str, ...] = ("id", "first_name", "last_name", "username")
    user: User = message.from_user
    user_data: str = " | ".join(str(value) for attr in user_attrs if (value := getattr(user, attr)))
    await message.answer(f"Hi there, {user_data}")
