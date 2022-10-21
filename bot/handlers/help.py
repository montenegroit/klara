import logging
from aiogram import Router, types
from bot.services.releases import get_last_release_version

logger = logging.getLogger(__name__)
router = Router()

_message = """
Вот список моих команд:
  /help - Получить данное сообщение
  
Список команд для супер админа:
  !ro - Дать бан
  
Список команд для донатеров:
  /prompt описание на англ - нагенерить изображения по тексту со stable diffusion

Хочешь увидеть меня бещ нечего - заходи <a href="https://github.com/montenegroit/klara"> сюда </a>

"""


@router.message(commands="help")
async def test_admin_message(message: types.Message):
    version = await get_last_release_version()
    await message.answer(_message + f"<i><a href='#'>{version}</a></i>")
