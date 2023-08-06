# coding=utf-8
"""
Common shared functions and classes
"""
from typing import Any, Optional

import aiohttp


async def getsecret(sname: str, fid: str, atoken: str) -> Optional[str]:
    """
    Returns the secret value from Yandex Cloud Lockbox

    :param sname: name of a secret
    :param fid: folderId of the cloud folder
    :param atoken: access token for Lockbox API
    :return: secret contents
    """
    async with aiohttp.ClientSession(raise_for_status=True) as s:
        async with s.get(f"GET https://lockbox.api.cloud.yandex.net/lockbox/v1/secrets?folderId={fid}",
                         headers={"Authorization": f"Bearer {atoken}"}) as r:
            _list = await r.json()
            for _s_item in _list["secrets"]:
                if _s_item["name"] == sname:
                    _sid = _s_item["id"]
                    async with s.get(f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{_sid}/payload",
                                     headers={"Authorization": f"Bearer {atoken}"}) as r:
                        _secret = await r.json()
                        return _secret["entries"][0]["textValue"]
    return None
