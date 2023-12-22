import asyncio
from typing import Any

from aiogram import types
from aiogram.types import WebhookInfo
from fastapi import FastAPI, status

import routing
from config import Config, get_config
from core import schemas as core_schemas
from meta import ProjectMeta
from tg.tg_bot import bot, dispatchers

config: Config = get_config()


def get_app() -> FastAPI:
    """Initializes and returns a FastAPI object"""
    project_meta: ProjectMeta = ProjectMeta()
    api: FastAPI = FastAPI(
        debug=config.app.debug,
        swagger_ui_parameters={"persistAuthorization": True},
        title=project_meta.title,
        description=project_meta.description,
        responses={status.HTTP_403_FORBIDDEN: {"model": core_schemas.ErrorSchema}},
        version=project_meta.version,
        **{"docs_url": None, "redoc_url": None} if not config.app.debug else {},
    )
    for prefix, routs in routing.AppRouter.routers:
        [api.include_router(router, prefix=prefix) for router in routs]
    return api


app: FastAPI = get_app()


@app.post(config.tg.webhook_path, include_in_schema=False)
async def webhook(update: dict[str, Any]) -> core_schemas.WebHookResponse:
    tg_update: types.Update = types.Update(**update)
    await dispatchers.base_dp.feed_update(bot=bot.bot, update=tg_update)
    return core_schemas.WebHookResponse()


@app.on_event("startup")
async def startup() -> None:
    if not config.app.debug:
        webhook_info: WebhookInfo = await bot.bot.get_webhook_info()
        if webhook_info.url != config.tg.webhook_url:
            await bot.bot.set_webhook(url=config.tg.webhook_url)
    else:
        asyncio.create_task(dispatchers.base_dp.start_polling(bot.bot))
