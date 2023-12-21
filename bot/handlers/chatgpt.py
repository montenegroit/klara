import g4f

from bot.config import config

HELP_TEXT = """ <b>клара, подскажи! <i>ваш текст</i></b> - Получить подсказку от ИИ\n"""


async def chatgpt_handler(data: dict):
    if data["command_data"].lower() == config.command_data_to_get_help:
        return HELP_TEXT

    abot = config.bot
    promt = data["message"]
    text_answer = (
        f"Дай ответ на запрос {promt}. Ответ не должен превышать 100 символов"
    )

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": text_answer,
                }
            ],
            stream=True,
        )
        message_list = []

        for message in response:
            message_list.append(message)

        reply_message = ''.join(message_list)

        return await data["message"].answer(reply_message)

    except RuntimeError:
        return 'Incorrect response'

    except:
        return 'Повторите запрос позже'
