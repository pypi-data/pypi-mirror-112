from outer.VirtualTerminal import VirtualTerminal
import os


class File:
    def __init__(self, path:str, is_dir=False):
        self.path = path
        self.is_dir = is_dir
        self.terminal = None
        # {} are replaced by args
        self.path_formatted = path

    def touch_(self, *args):
        self.path_formatted = self.path.format(*args)
        return self.touch()

    def touch(self):
        terminal = self.terminal
        fs = self.path_formatted.split(terminal.dir_delimiter)

        terminal.cd()
        if self.is_dir:
            left = None
        else:
            left = fs[-1]
            fs = fs[:-1]
        # create dir
        for f in fs:
            terminal.mkdir_enter(f)
        # solve left
        return os.path.join(terminal.pwd(), left) if left else terminal.pwd()

    def set_terminal(self, terminal):
        self.terminal = terminal
