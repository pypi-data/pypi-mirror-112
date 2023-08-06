"""
A sample to cover
"""
from BluePrintSample import BluePrintSample

# composite blueprint
blueprint = BluePrintSample('1')
# touch file or dir
out = blueprint.TRAIN_IMG_OUTPUT.touch()
# std out
print(out)
