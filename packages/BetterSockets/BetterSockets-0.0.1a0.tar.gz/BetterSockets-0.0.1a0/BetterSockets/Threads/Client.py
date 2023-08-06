from __future__ import annotations
import socket


class WebSocket:
    def __init__(self, **kwargs) -> WebSocket:
        self.__debug: bool = kwargs.get("debug", False)

        self.__port = int(kwargs.get("port", 5555))
        self.__Host = socket.gethostbyname(socket.gethostname())
        self.__buffer = int(kwargs.get("buffer", 1024))

        self.__Function = kwargs.get("func", None)

        self.__Socket = socket.socket()
        self.__debugPr(f"Opening connection on: {(self.__Host, self.__port)}")
        self.__Socket.connect((self.__Host, self.__port))

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

    def __del__(self):
        self.__Socket.send("!DISCONNECT".encode())
        self.__Socket.close()

    def send(self, data) -> send:
        self.__Socket.send(f"{data}".encode())
        self.__debugPr(f"Send message '{data}' to connection")

        if self.__Function:

            rec = self.__Socket.recv(self.__buffer)
            rec = rec.decode()

            self.__Function(rec)

    def reconnect(self) -> WebSocket:
        self.__Socket.send("!DISCONNECT".encode())
        self.__Socket.close()
        self.__debugPr(f"Reconnecting Socket")
        self.__Socket = socket.socket()
        self.__Socket.connect((self.__Host, self.__port))


# Client = WebSocket()
# Client.send("Test")
