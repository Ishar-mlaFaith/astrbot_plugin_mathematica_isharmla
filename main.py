from wolframclient.language import wl, wlexpr
import json
from functools import wraps
from typing import Iterable
import os

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *

from .manual import ManualSearcher
from .mathematica import MathematicaCore

@register("mathematica_isharmla", "Ishar-mlaFaith", "尝试实现让astrbot使用mma", "0.0.114")
class Isharmathematica(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.commands_and_functions_help_library = {}
        self.manual_searcher = ManualSearcher()
        self.mma_cores = {}
        
        self.config = config
        self.bot_config = context.get_config
        self.debug_prefix = config['debug_prefix']
        self.mma_prefix = config['mma_prefix']

        self.prefix_register()

    # @event_message_type(EventMessageType.ALL)
    # async def _message_middleware(self, event: AstrMessageEvent):
    #     '''消息处理中间件，用以进行命令识别。'''

    #     pass

    @filter.command("mmahelp")
    async def _send_manual_impl(self, event: AstrMessageEvent):
        '''本插件的帮助文档，请通过`/mmahelp`查看'''
        message_body = event.message_str.split('mmahelp')[1:]
        yield event.plain_result(self.manual_searcher.find(message_body))


    def prefix_register(self):
        # 更改触发词
        current_self = self        

        @wraps(current_self._specter_ping_impl)
        async def wrapper_specter_ping(_, event: AstrMessageEvent, *args, **kwargs):
            async for result in current_self._specter_ping_impl(event):
                yield result
        self.specter_ping = filter.command(command_name=f'{self.debug_prefix}ping')(wrapper_specter_ping)

    async def _specter_ping_impl(self, event: AstrMessageEvent):
        structure = {
            "message_str": str(event.message_str),
            "message_obj": str(event.message_obj),
            "platform_meta": str(event.platform_meta),
            "session": {
                "platform_name": str(event.session.platform_name),
                "message_type": str(event.session.message_type),
                "session_id": str(event.session.session_id)
            },
            "message_obj.raw_message" : event.message_obj.raw_message,
            "listdir": os.listdir(),
            "bot_config": {key: self.bot_config[key] if isinstance(self.bot_config[key], Iterable) else str(self.bot_config[key]) for key in self.bot_config}
        }
        yield event.plain_result(json.dumps(structure))


    # # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    # @filter.command("helloworld")
    # async def helloworld(self, event: AstrMessageEvent):
    #     '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
    #     user_name = event.get_sender_name()
    #     message_str = event.message_str # 用户发的纯文本消息字符串
    #     message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
    #     logger.info(message_chain)
    #     yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息
    #
    # async def terminate(self):
    #     '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
