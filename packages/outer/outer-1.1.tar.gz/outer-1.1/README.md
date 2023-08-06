# Outer

## 1. Installation

```
pip install outer
```

## 2 Method

A tool to manage output, which doesn't require you to create dir!


### 2.1. You must define a blueprint in this method
```
from outer.File import File
from outer.BluePrint import BluePrint


class BluePrintSample(BluePrint):
    def __init__(self):
        # define file or dir
        self.LOG_MAIN = File('run.log', is_dir=False)
        self.LOG_TENSORBOARD = File('event', is_dir=True)
        self.FILE_CHECKPOINT = File('model_{}.pkl', is_dir=False)
        self.TRAIN_IMG_OUTPUT = File('{}/train/image', is_dir=True)
        self.TRAIN_LABEL_OUTPUT = File('{}/train/label', is_dir=True)
        self.TRAIN_GT_OUTPUT = File('{}/train/gt', is_dir=True)
        # recall father init
        super().__init__()
```


### 2.2. Then you can simply use it with `touch` or `touch_` method!
```
from BluePrintSample import BluePrintSample

# composite blueprint
blueprint = BluePrintSample()
# touch file or dir
out = blueprint.TRAIN_IMG_OUTPUT.touch_(2)
# std out
print(out)
```