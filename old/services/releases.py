import logging

import httpx

from bot.config import config

logger = logging.getLogger(__name__)


def get_releases_url() -> str or None:
    if config.github_repo and config.github_token:
        return f"https://api.github.com/repos/{config.github_repo}/releases"


async def get_last_release_version() -> str or None:
    """
    :return:
    """

    url = get_releases_url()
    if not url:
        return

    headers = {
        "Authorization": f"Bearer {config.github_token}",
        "Accept": "application/vnd.github+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()[0]["tag_name"]

        logger.error(response.status_code, response.json())
