import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframCloudSession
from typing import Iterable
from astrbot.api.all import *

class MathematicaCore:
    def __init__(self, sender='default'):
        self.sender = sender
        self.canvas = {}
        self.wl = wl()
        self.session = WolframCloudSession(
            
        )

    def deal_with(self, event: AstrMessageEvent, rmsg:Iterable):
        if rmsg[0] == 'run':
            return self._run()
        elif rmsg[0] == 'canvas':
            type = 'mma'
            indent = 2
            for arg in rmsg[1:]:
                assert isinstance(arg, str)
                if arg.startwith('--type='):
                    type = arg[7:]
                elif arg.startswith('-t='):
                    type = arg[3:]
                elif arg.startswith('--indent='):
                    indent = arg[9:]
                elif arg.startswith('-i='):
                    indent = arg[3:]
            return self._canvas(type=type, indent=indent)
        elif rmsg[0].lower() in ['frun', 'fr', 'fastrun', 'fast_run'] and len(rmsg) > 1:
            if event.message_obj.raw_message['user_id'] == 206766382:
                return f'[DEBUG]MathematicaCore.deal_with `{str(rmsg)}` to get:\n' + str(self._fast_run(args=rmsg[1:]))


    def _run(self):
        pass

    def _canvas(self, type='mma', indent=2):
        pass

    def _fast_run(self, args):
        if result := self.session.evaluate([wlexpr(arg) for arg in args]):
            return result
        else:
            return self.session.evaluate(wlexpr(','.join(args)))
