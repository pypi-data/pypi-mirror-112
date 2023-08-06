# -*- coding: utf-8 -*-
"""
此模块定义机器人类，包含处于 model 层之下的 `SimpleMirai` 和建立在 model 层上的 `Mirai`。
"""
import asyncio
import logging
import sys
from typing import Callable, Type, Union

from mirai.adapters.base import Adapter, ApiProvider
from mirai.bus import EventBus
from mirai.models.api import ApiModel
from mirai.models.bus import ModelEventBus
from mirai.models.events import Event
from mirai.utils import async_, async_call_with_exception, asgi_serve


class SimpleMirai(ApiProvider):
    """
    基于 adapter 和 bus，处于 model 层之下的机器人类。

    使用了 `__getattr__` 魔术方法，可以直接在对象上调用 API。

    通过 `SimpleMirai` 调用 API 时，需注意此类不含 model 层封装，因此 API 名称与参数名称需与 mirai-api-http 中的定义相同，
    参数需要全部以具名参数的形式给出，并且需要指明使用的方法（GET/POST）。

    例如：
    ```py
    await bot.sendFriendMessage(target=12345678, messageChain=[
        {"type":"Plain", "text":"Hello World!"}
    ], method="POST")
    ```

    也可以使用 `call_api` 方法。

    对于名称的路由含有二级目录的 API，由于名称中含有斜杠，必须使用 `call_api` 调用，例如：
    ```py
    file_list = await bot.call_api("file/list", id="", target=12345678, method="GET")
    ```
    """
    def __init__(self, qq: int, adapter: Adapter):
        """
        `qq: int` QQ 号。

        `adapter: Adapter` 适配器，负责与 mirai-api-http 沟通，详见模块`mirai.adapters`。
        """
        self.qq = qq
        self._adapter = adapter
        self._bus = EventBus()
        self._adapter.register_event_bus(self._bus)

        self.setup_functions = []

        self.logger = logging.getLogger(__name__)

    async def call_api(self, api: str, **params):
        """调用 API。

        `api: str` API 名称。

        `**params` 参数。
        """
        return await async_(self._adapter.call_api(api, **params))

    def on(self, event: str, priority: int = 0) -> Callable:
        """注册事件处理器。

        `event: str` 事件名。

        `priority: int = 0` 优先级，较小者优先。

        用法举例：
        ```py
        @bot.on('FriendMessage')
        async def on_friend_message(event: dict):
            print(f"收到来自{event['sender']['nickname']}的消息。")
        ```
        """
        return self._bus.on(event, priority=priority)

    def setup(self, func: Callable) -> Callable:
        """注册机器人初始化处理器。"""
        self.setup_functions.append(func)
        return func

    async def _run_startup(self):
        """开始运行机器人（立即返回）。"""
        await self._adapter.login(self.qq)

        for func in self.setup_functions:
            await async_call_with_exception(func)

        self._adapter.start()

    async def _run_shutdown(self):
        """结束运行机器人。"""
        await self._adapter.logout()
        self._adapter.shutdown()

    async def _run(self):
        try:
            await self._run_startup()
            await self._adapter.background
        finally:
            await self._run_shutdown()

    @property
    def asgi(self):
        """返回 ASGI 实例，用于启动服务。"""
        asgi = self._adapter.asgi

        async def asgi_wrapper(scope, recv, send):
            if scope['type'] == 'lifespan':
                while True:
                    message = await recv()
                    if message['type'] == 'lifespan.startup':
                        await self._run_startup()
                        await send({'type': 'lifespan.startup.complete'})
                    elif message['type'] == 'lifespan.shutdown':
                        await self._run_shutdown()
                        await send({'type': 'lifespan.shutdown.complete'})
                        return
            else:
                return await asgi(scope, recv, send)

        return asgi_wrapper

    def run(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        asgi_server: str = 'auto',
        **kwargs
    ):
        """开始运行机器人。

        一般情况下，此函数会进入主循环，不再返回。
        """
        if not asgi_serve(
            self.asgi, host=host, port=port, asgi_server=asgi_server, **kwargs
        ):
            logger = logging.getLogger(__name__)
            logger.warning(
                """未找到可用的 ASGI 服务，反向 WebSocket 和 WebHook 上报将不可用。
建议安装 ASGI 服务器，如 `uvicorn` 或 `hypercorn`。
在命令行键入：
    pip install uvicorn
或者
    pip install hypercorn"""
            )
            try:
                asyncio.run(self._run())
            except KeyboardInterrupt:
                sys.exit(0)


class Mirai(SimpleMirai):
    """
    机器人主类。

    使用了 `__getattr__` 魔术方法，可以直接在对象上调用 API。

    `Mirai` 类包含 model 层封装，API 名称经过转写以符合命名规范，所有的 API 全部使用小写字母及下划线命名。
    （API 名称也可使用原名。）
    API 参数可以使用具名参数，也可以使用位置参数，关于 API 参数的更多信息请参见模块 `mirai.models.api`。

    例如：
    ```py
    await bot.send_friend_message(12345678, [
        Plain("Hello World!")
    ])
    ```

    也可以使用 `call_api` 方法，须注意此方法直接继承自 `SimpleMirai`，因此未经 model 层封装，
    需要遵循 `SimpleMirai` 的规定。
    """
    def __init__(self, qq: int, adapter: Adapter):
        super().__init__(qq=qq, adapter=adapter)
        # 将 bus 更换为 ModelEventBus
        adapter.unregister_event_bus(self._bus)
        self._bus = ModelEventBus()
        adapter.register_event_bus(self._bus.base_bus)

    def on(
        self,
        event_type: Union[Type[Event], str],
    ) -> Callable:
        """注册事件处理器。

        `event_type: Union[Type[Event], str]` 事件类或事件名。

        `priority: int = 0` 优先级，较小者优先。

        用法举例：
        ```python
        @bot.on(FriendMessage)
        async def on_friend_message(event: FriendMessage):
            print(f"收到来自{event.sender.nickname}的消息。")
        ```
        """
        return self._bus.on(event_type=event_type)

    def api(self, api: str) -> ApiModel.Proxy:
        """获取 API Proxy 对象。

        API Proxy 提供更加简便的调用 API 的写法，详见`mirai.models.api`。

        `Mirai` 的 `__getattr__` 与此方法完全相同，可支持直接在对象上调用 API。

        `api: str` API 名称。
        """
        api_type = ApiModel.get_subtype(api)
        return api_type.Proxy(self, api_type)

    def __getattr__(self, api: str) -> ApiModel.Proxy:
        return self.api(api)
