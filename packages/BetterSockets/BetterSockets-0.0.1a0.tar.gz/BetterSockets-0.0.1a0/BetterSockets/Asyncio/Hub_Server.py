import asyncio
import json


class WebSocket:
    def __init__(self, **kwargs):
        self.__debug: bool = kwargs.get("debug", False)

        self.__port: int = kwargs.get("port", 8888)
        self.__ip: str = kwargs.get("ip", "127.0.0.1")

        self.__Reader, self.__Writer = None, None

        self.__identification = kwargs.get("identifier", None)
        self.__Clients = []

        self.__Server = None

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

    def __remove(self, writer):
        try:
            self.__Clients.remove(writer)
        except Exception:
            return

    def listen(self):
        asyncio.run(self.__listeningPrep())

    async def __listeningPrep(self):
        self.__debugPr(f"Starting server on: {self.__ip, self.__port}")
        self.__Server = await asyncio.start_server(self.__listen, self.__ip, self.__port)

        async with self.__Server:
            await self.__Server.serve_forever()

    async def __listen(self, reader, writer):
        addr = writer.get_extra_info('peername')

        data = await reader.read(100)
        data = data.decode()
        self.__debugPr(f"Message from address {addr} received: '{data}'")
        if self.__identification:
            retr = self.__identification(data)

            if retr[0] is False:
                self.__debugPr(f"Closing connection to address {addr}")
                self.__remove(writer)
                return

        self.__Clients.append(writer)

        for client in self.__Clients:
            if self.__identification:
                client.write(json.dumps({'Address': addr, 'User': retr[1], 'Message': data}).encode())
                await client.drain()

            else:
                client.write(json.dumps({'Address': addr, 'Message': data}).encode())
                await client.drain()

            self.__debugPr(f"Send message to address: {client.get_extra_info('peername')}")
