# frame_count

import os
import cv2
import numpy as np
from LivestockCV.core import plot_image
from LivestockCV.core import print_image
from LivestockCV.core import params


def frame_count(video):
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return print(length)