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

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.ChatBase,
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

    return await data["message"].ansewr(reply_message)

# response = g4f.Completion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Hello"}],
#     stream=True,
# )
#
# for message in response:
#     print(message, flush=True, end='')
#
#
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "Hello"}],
# )
#
# print(response)
