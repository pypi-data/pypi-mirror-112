
from asyncio.streams import StreamReader


class TcpProtoBase:
    def make_heart_msg(self) -> bytes:
        pass

    def build_msg(self, data:bytes) -> bytes:
        pass

    async def read_msg(self, reader: StreamReader):
        pass
