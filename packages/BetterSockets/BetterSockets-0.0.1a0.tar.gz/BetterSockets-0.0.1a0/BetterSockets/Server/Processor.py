from __future__ import annotations
from socket import socket

# Importing the different types of Process_Server
from BetterSockets.Asyncio.Process_Server import WebSocket as AsyncSocket
from BetterSockets.Threads.Process_Server import WebSocket as ThreadSocket


class ProcessorServer:
    def __init__(self, **kwargs) -> socket:
        self.__type: bool = kwargs.get("is_async", False)

        if self.__type is True:
            self.__Socket = AsyncSocket(**kwargs)

        elif self.__type is False:
            self.__Socket = ThreadSocket(**kwargs)

    def listen(self):
        self.__Socket.listen()
