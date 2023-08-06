from outer.VirtualTerminal import VirtualTerminal
from outer.File import File


class BluePrint:
    def __init__(self, root_dir='log', key:str = None):
        self._root_dir = 'log'
        # default to init
        self.init(root_dir=root_dir, key=key)

    def init(self, root_dir='log', key:str = None):
        self._root_dir = root_dir
        terminal = VirtualTerminal(root=root_dir, key=key)
        # set terminal
        for name, obj in vars(self).items():
            if type(obj) is File:
                obj.set_terminal(terminal)
        return self