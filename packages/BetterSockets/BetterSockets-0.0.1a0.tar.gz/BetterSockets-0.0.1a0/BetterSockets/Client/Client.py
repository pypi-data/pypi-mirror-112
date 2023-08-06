from __future__ import annotations
from socket import socket

# Importing the different types of Hub_Server
from BetterSockets.Asyncio.Client import WebSocket as AsyncClient
from BetterSockets.Threads.Client import WebSocket as ThreadClient


class Client:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = AsyncClient(**kwargs)

        elif self.__type is False:
            self.__Socket = ThreadClient(**kwargs)

    def send(self, data: str):
        self.__Socket.send(data)
