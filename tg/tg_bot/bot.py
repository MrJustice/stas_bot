from aiogram import Bot

from config import Config, get_config

config: Config = get_config()

bot: Bot = Bot(token=config.tg.token, parse_mode=config.tg.parse_mode)
