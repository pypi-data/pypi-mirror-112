import asyncio
import json
from typing import Callable
from l0n0ltcp.tcp_proto_base import TcpProtoBase
from l0n0ltcp.tcp_session_mgr import TcpSessionMgr


class TcpClient:
    def __init__(self,
                 host: str,
                 port: int,
                 msg_handler: Callable,
                 proto: TcpProtoBase,
                 heartbeat_interval: float = 0,
                 max_no_msg_count: int = 0,
                 loop=None):
        self.loop = loop or asyncio.get_running_loop()
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.autoreconnect = False
        self.session_mgr = TcpSessionMgr(msg_handler,
                                         proto,
                                         heartbeat_interval,
                                         max_no_msg_count)

    async def _start(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port, loop=self.loop)
        self.session_mgr.on_new_session(self.reader, self.writer)

    def start(self):
        self.loop.create_task(self._start())

    def close(self):
        self.session_mgr.close()

    def send_msg(self, data: bytes):
        for session in self.session_mgr.sessions.values():
            session.send_msg(data)

    def send_json(self, data: dict):
        return self.send_msg(json.dumps(data).encode())

    def enable_auto_reconnect(self, retry_interval: float):
        if not self.autoreconnect:
            return

        if self.writer.is_closing():
            self.start()

        self.loop.call_later(retry_interval, self.enable_auto_reconnect)

    def distable_auto_reconnect(self):
        self.autoreconnect = False
