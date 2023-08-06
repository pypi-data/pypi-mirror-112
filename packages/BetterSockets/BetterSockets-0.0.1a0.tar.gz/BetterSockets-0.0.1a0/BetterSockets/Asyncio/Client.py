import asyncio


class WebSocket:
    def __init__(self, **kwargs):
        self.__debug: bool = kwargs.get("debug", False)

        self.__port: int = kwargs.get("port", 8888)
        self.__ip: str = kwargs.get("ip", "127.0.0.1")

        self.__Reader, self.__Writer = None, None
        self.__func = kwargs.get("func", None)

    def send(self, data):
        asyncio.run(self.__send(data))

    def __debugPr(self, Input: str):
        if self.__debug is True:
            print(f"[DEBUG] :: {Input}")

    async def __send(self, data):
        self.__debugPr(f"Opening connection through asyncio on: {self.__ip, self.__port}")
        self.__Reader, self.__Writer = await asyncio.open_connection(self.__ip, self.__port)

        self.__Writer.write(f"{data}".encode())
        await self.__Writer.drain()
        self.__debugPr(f"Send message '{data}' to connection")

        if self.__func:
            _data = await self.__Reader.read(100)
            if _data:
                self.__debugPr(f"Message received: '{_data}'")
                retr = self.__func(_data)
                if retr:
                    self.__debugPr(f"Send message '{retr}' to connection")
                    self.__Writer.write(bytes(retr, "utf-8"))

        self.__Writer.close()


# Cl = WebSocket()
# Cl.send("Test")
