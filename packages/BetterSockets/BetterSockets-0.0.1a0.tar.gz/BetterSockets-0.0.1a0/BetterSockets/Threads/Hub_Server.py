from __future__ import annotations
import socket
from threading import Thread
import json


class WebSocket:
    def __init__(self, **kwargs) -> WebSocket:
        self.__debug: bool = kwargs.get("debug", False)

        self.__port = int(kwargs.get("port", 5555))
        self.__Host = "0.0.0.0"
        self.__buffer = int(kwargs.get("buffer", 1024))

        self.__Socket = socket.socket()
        self.__bind()

        self.__Clients = []
        self.__identification = kwargs.get("identifier", None)

    def __del__(self):
        self.__Socket.close()

    def __bind(self) -> socket:
        self.__Socket.bind((self.__Host, self.__port))

    def listen(self) -> Thread:
        self.__Socket.listen(1)

        while True:
            conn, addr = self.__Socket.accept()
            thread = Thread(target=self.__flag, args=[conn, addr])
            thread.start()

    def __remove(self, client: tuple):
        try:
            self.__Clients.remove(client)
        except Exception:
            return

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

    def __flag(self, conn, addr):
        if self.__identification:
            try:
                msg = conn.recv(self.__buffer)
            except socket.error():
                pass
            msg = msg.decode()

            self.__debugPr(f"Message from address {addr} received: '{msg}'")

            retr = self.__identification(msg)

            if retr[0] is False:
                conn.send("!DISCONNECT".encode())
                self.__remove((conn, addr))
                conn.close()
                self.__debugPr(f"Closed connection to address: {addr}")
                return

        self.__Clients.append((conn, addr))

        while True:
            try:
                msg = conn.recv(self.__buffer)
            except socket.error():
                break
            msg = msg.decode()
            if msg == "!DISCONNECT":
                self.__remove((conn, addr))
                conn.close()
                self.__debugPr(f"Closed connection to address: {addr}")
                break

            for client in self.__Clients:
                if self.__identification:
                    client[0].send(json.dumps({'Address': addr, 'User': retr[1], 'Message': msg}).encode())
                else:
                    client[0].send(json.dumps({'Address': addr, 'Message': msg}).encode())

                self.__debugPr(f"Send message to address: {client[1]}")


# Hub = WebSocket()
# Hub.listen()
