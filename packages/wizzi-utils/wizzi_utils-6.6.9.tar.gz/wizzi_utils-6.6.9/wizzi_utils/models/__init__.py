"""
:requires: cv2
    pip install opencv-python
:requires: tflite_runtime
    winOs: pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
:sub_package: wizzi_utils.pyplot
:sub_package: wizzi_utils.open_cv
:sub_package: wizzi_utils.socket_tools
"""
try:
    from wizzi_utils.models.models import *
    from wizzi_utils.models import object_detection as od
    from wizzi_utils.models import pose_detection as pd
except ModuleNotFoundError as e:
    pass

from wizzi_utils.models import test
