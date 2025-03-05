from wolframclient.language import wl, wlexpr
import json

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("mathematica_isharmla", "Ishar-mlaFaith", "尝试实现让astrbot使用mma", "1.0.0")
class Isharmathematica(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.commands_and_functions_help_library = {}

    def manual_structurer(self, command_name: str, from_library: dict):
        return "施工中"

    def help_plain_text(self, command_name: str, *args):
        cn = command_name.lower()
        if cn not in self.commands_and_functions_help_library:
            return "该命令尚不存在帮助文档" # command_name不存在帮助文档时回复
        else:
            # 先输出command_name下帮助文档结构
            command_name_structure_description = f'以下是`{command_name}`的帮助文档结构\n{self.manual_structurer(cn, self.commands_and_functions_help_library)}'

            # 再输出特定*args下的帮助文档
            detailed_args_description = ''
            if len(args):
                helper
                for i in range(len(args)):


            return command_name_structure_description + '\n--------分割线--------\n' + detailed_args_description


    @filter.command("mmahelp")
    async def send_manual(self, event: AstrMessageEvent, *args):
        '''无参数时回复本插件使用手册；有参数时尝试回复参数描述的命令的帮助文档'''

        if len(args) == 0:
            # 无参数，回复本插件使用手册
            manual = '''
                Mathematica（俗称mma）是一个高效且强大的数学运算软件，且公开了官方python库。
                本插件基于该库，故用户最好拥有一定的mma基础。不过即使没有也可以轻松上手完成工作学习生活上大部分数学计算需要。
                您可以输入`/mmahelp <命令>`来获取对应命令或函数的帮助文档。如`/mmahelp plot`
            '''.strip()
            yield event.plain_result(manual)
        elif help_plain_text_content := self.help_plain_text(args):
            yield event.plain_result(help_plain_text_content)

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
