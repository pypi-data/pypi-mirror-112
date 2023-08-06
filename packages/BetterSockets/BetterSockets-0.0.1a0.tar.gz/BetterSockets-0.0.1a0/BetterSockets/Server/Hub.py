from __future__ import annotations
from socket import socket

# Importing the different types of Hub_Server
from BetterSockets.Asyncio.Hub_Server import WebSocket as AsyncHub
from BetterSockets.Threads.Hub_Server import WebSocket as ThreadHub


class HubServer:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = AsyncHub(**kwargs)

        elif self.__type is False:
            self.__Socket = ThreadHub(**kwargs)

    def listen(self):
        self.__Socket.listen()
