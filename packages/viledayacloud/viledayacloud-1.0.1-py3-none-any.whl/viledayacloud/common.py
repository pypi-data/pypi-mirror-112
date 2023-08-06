# coding=utf-8
"""
Common shared functions and classes
"""
from typing import Any

import aiohttp


async def getsecret(sid: str, context: Any) -> str:
    """
    Returns the secret value from Yandex Cloud Lockbox

    :param sid: ID of a secret
    :param context: Yandex Function call context
    :return: secret contents
    """
    async with aiohttp.ClientSession() as s:
        async with s.get(f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{sid}/payload",
                         headers={"Authorization": f"Bearer {context.token['access_token']}"}) as r:
            _json = await r.json()
    return _json["entries"][0]["textValue"]
