import logging

from aiogram import Router, types

logger = logging.getLogger(__name__)
router = Router()


temp_count = 0  # TODO: mb use redis?
reminder_text = """<b>Напоминалочка</b>
» Уважайте себя и <a href='https://media-exp2.licdn.com/dms/image/C4D16AQElG9kR0NMaUA/profile-displaybackgroundimage-shrink_200_800/0/1644345282801?e=1663804800&v=beta&t=kuIy126VZBAeO7-OAsb475xvAyjHoTddOfCUw-eg4l0'>других</a>
» Подробные <a href='https://github.com/63phc/montenegro_it'>правилами чата</a>
» Чат тематический, оффтоп сообщения (не относящиеся к IT в Черногории и близким к ней темам) разрешены только при отсутствии активных обсуждений по тематике чата, оффтоп не должен мешать разговорам по теме чата

» <b>Если вы в readonly, попробуйте выйти, зайти и пройти тест заново</b>

<b>Проекты:</b>
» <a href='https://digitalmonte.notion.site/Startup-Factory-b14d4371b4854a989bb104df47e9a8e8'>Startup Factory Montenegro</a>
» Чат по вопросам <a href='https://t.me/montenegro_porez'>ВНЖ/Налогов/Фирм</a>
» Чат коворкинга в Будве в <a href='https://t.me/Itbranchhouse'>Itbranchhouse</a>
» Самый нужный бот в ЧГ <a href='https://t.me/MontenegroDoctorsBot'>MontenegroDoctorsBot</a>

<b>Подписывайтесь на наши соц.сети и каналы:</b>
» <a href='https://www.facebook.com/groups/montenegroit'>Фото с митапов в ФБ</a>
» <a href='https://www.youtube.com/channel/UCdpRn1SqfqHDFJIrhZb9lsw'>YouTube</a>
» <a href='https://speakerdeck.com/montenegro_it'>Презентации с митапов </a>
» <a href='https://t.me/montenegro_it_events'>Канал с ивентами</a>
» <a href='https://t.me/montenegro_it_jobs'>Канал с вакансиями</a>

<b>Когда митап?</b>
» 28-29 января в Сплендиде
» Будет на английском, вход 15 евро
» https://montenegroit.github.io/meetup/

Не забываем <a href='https://t.me/montenergo_it/47783'>донатить</a> на монтаж видео с митапов и пиво админам.
Вы получите уникальную подпись, и возможность использовать расширенные команды бота в /help
"""


@router.message()
async def temp_reminder_100(message: types.Message):
    global temp_count
    if temp_count > 100:
        await message.answer(reminder_text)
        temp_count = 0
    else:
        temp_count += 1
