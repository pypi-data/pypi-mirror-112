import asyncio
import struct
import json
import logging
from typing import Callable
from l0n0ltcputils.tcp_proto_base import TcpProtoBase


class TcpSession:
    def __init__(self,
                 owner,
                 id: int,
                 r: asyncio.StreamReader,
                 w: asyncio.StreamWriter,
                 heart_interval: float,
                 max_no_msg_count: int,
                 proto: TcpProtoBase,
                 msg_handler: Callable) -> None:
        self.owner = owner
        self.id = id
        self.reader = r
        self.writer = w
        self.proto = proto
        self.msg_handler = msg_handler
        self.heart_interval = heart_interval
        self.max_no_msg_count = max_no_msg_count
        self.no_msg_count = 0

    def _heart(self):
        try:
            if self.writer.is_closing() or self.heart_interval <= 0:
                return

            if self.max_no_msg_count > 0:
                self.no_msg_count += 1
                if self.no_msg_count >= self.max_no_msg_count:
                    self.writer.close()

            heart_msg = self.proto.make_heart_msg()
            if heart_msg:
                self.writer.write(heart_msg)

            asyncio.get_event_loop().call_later(self.heart_interval, self._heart)
        except:
            pass

    def start_heart(self):
        if self.writer.is_closing() or self.heart_interval <= 0:
            return
        asyncio.get_event_loop().call_later(self.heart_interval, self._heart)

    async def run(self):
        try:
            while not self.writer.is_closing():
                msg_data = await self.proto.read_msg(self.reader)
                self.no_msg_count = 0
                if msg_data is None:
                    continue
                ret = await self.msg_handler(self.id, msg_data)
                if ret is None:
                    continue
                self.send_msg(ret)
        except Exception as e:
            logging.error(e.with_traceback(None))
        await self.owner.on_session_close(self.id)

    def send_msg(self, data: bytes):
        try:
            data = self.proto.build_msg(data)
            self.writer.write(data)
        except Exception as e:
            logging.error(f"send msg error: {e.with_traceback(None)}")
            return False
        return True


class TcpSessionMgr:
    def __init__(self,
                 msg_handler: Callable,
                 proto: TcpProtoBase,
                 heartbeat_interval: float = 0,
                 max_no_msg_count: int = 0) -> None:
        self.sessions = {}
        self.max_session_id = 0
        self.handlers = {}
        self.msg_handler = msg_handler
        self.proto = proto
        self.heartbeat_interval = heartbeat_interval
        self.max_no_msg_count = max_no_msg_count

    async def on_new_session(self, r: asyncio.StreamReader, w: asyncio.StreamWriter):
        self.max_session_id += 1
        session = TcpSession(self,
                             self.max_session_id,
                             r, w,
                             self.heartbeat_interval,
                             self.max_no_msg_count,
                             self.proto,
                             self.msg_handler)
        self.sessions[self.max_session_id] = session
        session.start_heart()
        await session.run()

    async def on_session_close(self, id: int):
        del self.sessions[id]
