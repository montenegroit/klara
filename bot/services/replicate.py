import logging

import httpx
import replicate
from replicate.exceptions import ModelError, ReplicateError

from bot.config import config

logger = logging.getLogger(__name__)
r = replicate.Client(api_token=config.replicate_api_token)


def get_replicate(prompt: str) -> str:
    try:
        model = r.models.get("stability-ai/stable-diffusion")
    except ModelError:
        return "NSFW content detected. Try running it again, or try a different prompt."
    except ReplicateError:
        return "Limit"
    output = model.predict(prompt=prompt)
    return output
