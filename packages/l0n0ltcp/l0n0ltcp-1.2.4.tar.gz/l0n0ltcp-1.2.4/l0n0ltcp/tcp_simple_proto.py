import struct
from l0n0ltcp.tcp_proto_base import TcpProtoBase, StreamReader


class TcpSimpleProto(TcpProtoBase):
    def make_heart_msg(self) -> bytes:
        return b"\x00\x00\x00"

    def build_msg(self, data: bytes) -> bytes:
        data_len = len(data) + 4
        size = data_len & 0xFFFF
        count = (data_len >> 16) & 0xFF
        header = struct.pack("!HBI", size, count, 0)
        return header + data

    async def read_msg(self, reader: StreamReader):
        header = await reader.readexactly(3)
        size, count = struct.unpack("!HB", header)
        size = (count << 16) | size
        if size <= 0:
            return
        return await reader.readexactly(size)
