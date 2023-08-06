from __future__ import annotations
import socket
from threading import Thread


class WebSocket:
    def __init__(self, **kwargs) -> WebSocket:
        self.__debug: bool = kwargs.get("debug", False)

        self.__port = int(kwargs.get("port", 5555))
        self.__Host = "0.0.0.0"
        self.__buffer = int(kwargs.get("buffer", 1024))

        self.__Socket = socket.socket()
        self.__bind()

        self.__Function = kwargs.get("func", None)

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

    def __del__(self):
        self.__Socket.close()

    def __bind(self) -> socket:
        self.__Socket.bind((self.__Host, self.__port))

    def listen(self) -> Thread:
        self.__Socket.listen(1)

        while True:
            conn, addr = self.__Socket.accept()
            self.__debugPr(f"Starting Thread for incoming connection")
            thread = Thread(target=self.__flag, args=[conn, addr])
            thread.start()

    def __flag(self, conn, addr):
        while True:
            try:
                msg = conn.recv(self.__buffer)
            except socket.error():
                break
            msg = msg.decode()
            self.__debugPr(f"Message from address {addr} received: '{msg}'")

            if msg == "!DISCONNECT":
                self.__debugPr(f"Closed connection to address: {addr}")
                conn.close()
                break

            if self.__Function:
                retr = self.__Function(msg)
                if retr:
                    if retr != "!DISCONNECT":
                        conn.send(f"{retr}".encode())
                        self.__debugPr(f"Closed connection to address: {addr}")
                        conn.close()

                    else:

                        self.__debugPr(f"Send Message: '{retr}' to address: {addr}")
                        conn.send(f"{retr}".encode())


# Server = WebSocket()
# Server.listen()
