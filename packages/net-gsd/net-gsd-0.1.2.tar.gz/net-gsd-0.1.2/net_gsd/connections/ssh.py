from typing import Union, Dict
from contextlib import asynccontextmanager

from scrapli.driver import AsyncDriver
from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver
from scrapli.response import Response

from net_gsd.connections.base import Base

PLATFORM = {"ios": AsyncIOSXEDriver, "nxos": AsyncNXOSDriver}


class SSH(Base):
    _con: AsyncDriver = None

    def __init__(self, host: str, username: str, password: str, platform: str, enable: str) -> None:
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.enable: str = enable
        self.platform: str = platform

        self.get_driver()

    def get_driver(self) -> None:
        self._con = PLATFORM.get(self.platform)(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_secondary=self.enable,
            auth_strict_key=False,
            transport="asyncssh",
        )

    @asynccontextmanager
    async def get_connection(self):
        await self._con.open()
        yield self
        await self._con.close()

    async def send_command(self, cmd: str, parse: bool = True) -> Union[Dict, str]:
        result: Response = await self._con.send_command(cmd)
        if parse:
            return result.genie_parse_output()
        return result.result
