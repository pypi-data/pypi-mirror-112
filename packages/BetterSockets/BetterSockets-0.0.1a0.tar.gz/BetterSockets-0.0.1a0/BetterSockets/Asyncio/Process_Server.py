import asyncio


class WebSocket:
    def __init__(self, **kwargs):
        self.__debug: bool = kwargs.get("debug", False)

        self.__port: int = kwargs.get("port", 8888)
        self.__ip: str = kwargs.get("ip", "127.0.0.1")

        self.__Reader, self.__Writer = None, None

        self.__func = kwargs.get("func", None)
        self.__Server = None

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

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

        if self.__func:
            retr = self.__func(data)

            if retr:
                writer.write(f"{retr}".encode())
                await writer.drain()
                self.__debugPr(f"Send message '{retr}' to address: {addr}")
