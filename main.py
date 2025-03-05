from wolframclient.language import wl, wlexpr
import json
from functools import wraps

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

from .manual import ManualSearcher

@register("mathematica_isharmla", "Ishar-mlaFaith", "尝试实现让astrbot使用mma", "0.0.114")
class Isharmathematica(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.commands_and_functions_help_library = {}
        self.manual_searcher = ManualSearcher()
        self.config = config
        self.debug_prefix = config['debug_prefix']
        self.debug_register()

    @filter.command("mmahelp")
    async def send_manual(self, event: AstrMessageEvent):
        message_obj = event.message_obj

    def debug_register(self):
        # 更改debug方法的触发词
        current_self = self

        @wraps(current_self._specter_ping_impl)
        async def wrapper_specter_ping(_, event: AstrMessageEvent, *args, **kwargs):
            return await current_self._specter_ping_impl(event)

        self.specter_ping = filter.command(command_name=f'{self.debug_prefix}ping')(wrapper_specter_ping)

    async def _specter_ping_impl(self, event: AstrMessageEvent):
        yield event.plain_result(
            f'AstrMessageEvent structure:\n' +
            f'message_str: {event.message_str}' +
            f'message_obj: {event.message_obj}' +
            f'platform_meta: {event.platform_meta}' +
            f'session:\n'
            f'  platform_name: {event.session.platform_name}' +
            f'  message_type: {event.session.message_type}' +
            f'  session_id: {event.session.session_id}'
        )


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
