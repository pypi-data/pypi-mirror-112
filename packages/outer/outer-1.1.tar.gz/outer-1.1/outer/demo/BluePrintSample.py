from outer.File import File
from outer.BluePrint import BluePrint


class BluePrintSample(BluePrint):
    def __init__(self, key='1'):
        # define file or dir
        self.LOG_MAIN = File('run.log', is_dir=False)
        self.LOG_TENSORBOARD = File('event', is_dir=True)
        self.FILE_CHECKPOINT = File('model_{}.pkl', is_dir=False)
        self.TRAIN_IMG_OUTPUT = File('train/image', is_dir=True)
        self.TRAIN_LABEL_OUTPUT = File('train/label', is_dir=True)
        self.TRAIN_GT_OUTPUT = File('train/gt', is_dir=True)
        # recall father init
        super().__init__(key=key)