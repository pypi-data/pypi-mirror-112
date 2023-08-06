import os
import datetime as dt


class VirtualTerminal:
    def __init__(self, root='log', dir_delimiter=os.sep, key:str = None):
        # status
        self.current_dir = '.'
        # init
        self.dir_delimiter = dir_delimiter

        self.check_dir(root)
        if key is not None:
            self.root_dir = os.path.join(root, key)
            self.check_dir(self.root_dir)
        else:
            self.root_dir = root

        # status info
        self.current_dir = self.root_dir

    def get_root(self):
        """
        :return: base dir of log
        """
        return self.root_dir

    def pwd(self):
        """
        :return: the pointer of current dir
        """
        return self.current_dir

    def mkdir(self, dir):
        """
        :param dir: dir to create and return create dir, but not modify the current dir
        :return: self.current_dir/dir
        """
        self.check_dir(dir)
        self.current_dir = os.path.join(self.current_dir, dir)
        return self

    def mkdir_enter(self, dir):
        """
        :param dir: dir to create and return create dir, then modify the current dir
        :return: self.current_dir/dir
        """
        self.check_dir(dir)
        self.current_dir = os.path.join(self.current_dir, dir)
        return self

    def cd(self, dir=None):
        if dir is None:
            self.current_dir = self.get_root()
        elif dir == '..':
            dirs = self.current_dir.split(self.dir_delimiter)
            if len(dirs) > 2:
                dirs = dirs[:-1]
                self.current_dir = self.dir_delimiter.join(dirs)
        else:
            path = os.path.join(self.current_dir, dir)
            if os.path.exists(path):
                self.current_dir = path
        return self

    def new_file(self, file):
        """
        :param file: the file to create
        :return: the path of file
        """
        return os.path.join(self.current_dir, file)

    def _get_current_datetime(self):
        """
        :return: current datetime
        """
        return dt.datetime.now().strftime('%Y%m%d_%H%M%S')

    def check_dir(self, root):
        cur_dir = os.path.join(self.current_dir, root)
        if not os.path.exists(cur_dir):
            os.mkdir(cur_dir)


if __name__ == '__main__':
    terminal = VirtualTerminal()
    print(terminal.pwd())