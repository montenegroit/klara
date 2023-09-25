import logging
import re

import httpx
import replicate
from aiogram import Bot, Router, types
from replicate.exceptions import ModelError, ReplicateError

from bot.config import config

logger = logging.getLogger(__name__)
r = replicate.Client(api_token=config.replicate_api_token)
router = Router()


@router.message()
async def prompt(message: types.Message):
    abot = config.bot

    # member = await abot.get_chat_member(
    #     chat_id=message.chat.id,
    #     user_id=message.from_user.id,
    # )

    # print(f"prompt: {message.text}")
    if (
        message.text
        and "prompt" in message.text
        # and isinstance(member, (types.ChatMemberOwner, types.ChatMemberAdministrator))
    ):
        prompt_list = message.text.split()
        output = get_replicate(" ".join(prompt_list[1:]))
        if len(output) > 0 and output[0].startswith("https://"):
            photo = types.URLInputFile(url=output[0])
            return await abot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_to_message_id=message.message_id,
            )
        return await message.answer(output)


def get_replicate(prompt: str) -> str:
    try:
        # model = r.models.get("stability-ai/stable-diffusion")
        output = r.run(
            config.prompt_replicate_model,
            input={"prompt": prompt},
        )
    except ModelError as exception:
        msg = f"ModelError: NSFW content detected. Try running it again, or try a different prompt. {exception}"
        logger.warning(msg)
        return msg
    except ReplicateError as exception:
        msg = f"ReplicateError: {exception}"
        logger.warning(msg)
        return msg

    # output = model.predict(prompt=prompt)
    print(f"{output}")
    return output  # [0]
