import logging

import httpx
import replicate
from replicate.exceptions import ModelError, ReplicateError

from bot.config import config

logger = logging.getLogger(__name__)
r = replicate.Client(api_token=config.replicate_api_token)


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
