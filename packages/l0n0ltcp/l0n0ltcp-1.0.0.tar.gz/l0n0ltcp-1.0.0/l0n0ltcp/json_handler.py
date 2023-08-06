import logging
import asyncio
import json

wait_futures = {}
max_serial_id = 0


def gen_serial_id():
    global max_serial_id
    max_serial_id += 1
    return max_serial_id


class JsonHandler:
    def __init__(self, ) -> None:
        self._handlers = {}

    def regist_handler(self, fn):
        self._handlers[fn.__name__] = fn

    async def __call__(self, id, data):
        data: dict = json.loads(data[4:], encoding="utf8")

        func_name = data.get("name")
        args = data.get("args")

        # 检查参数
        if func_name is None or args is None:
            return

        # 检查是否是返回值
        fu: asyncio.Future = wait_futures.get(func_name)
        if fu is not None:
            fu.set_result(args)
            return

        func = self._handlers.get(func_name)
        if func is None:
            logging.error(f"no such handler named {func_name}")
            return

        ret = await func(id, *args)
        serial_id = data.get("serial_id")
        if serial_id:
            return json.dumps({
                "name": serial_id,
                "args": ret
            }).encode()


class JsonRpc:
    def __init__(self, server) -> None:
        self.server = server

    async def __call__(self, id, name, *args, has_return=False):
        if has_return:
            serial_id = gen_serial_id()
            ret = asyncio.Future(asyncio.get_event_loop())
            wait_futures[serial_id] = ret
            if not self.server.send_json(id, {"name": name,
                                              "args": args,
                                              "serial_id": serial_id}):
                logging.error(
                    f"call server function [{name}] error: send msg error!"
                )
                return
            try:
                return await asyncio.wait_for(ret, 5)
            except asyncio.TimeoutError:
                logging.error(f"call server function [{name}] error: timeout!")
                return
        else:
            return self.server.send_json(id, {"name": name, "args": args})
