import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession
from typing import Iterable

class MathematicaCore:
    def __init__(self, sender='default'):
        self.sender = sender
        self.canvas = {}
        self.wl = wl()
        self.session = WolframLanguageSession()

    def deal_with(self, rmsg:Iterable):
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
            return self._fast_run(args=rmsg[1:])


    def _run(self):
        pass

    def _canvas(self, type='mma', indent=2):
        pass

    def _fast_run(self, args):
        return self.session.evaluate([wlexpr(arg) for arg in args])
