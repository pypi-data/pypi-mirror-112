# Apply White or Black Background Mask

import os
import cv2
import numpy as np
from LivestockCV.core import params
from LivestockCV.core import plot_image
from LivestockCV.core import print_image
from LivestockCV.core import fatal_error
from LivestockCV.core.transform import rescale


def apply_mask(img, mask, mask_color):


    params.device += 1

    if mask_color.upper() == "WHITE":
        color_val = 255
    elif mask_color.upper() == "BLACK":
        color_val = 0
    else:
        fatal_error('Mask Color ' + str(mask_color) + ' is not "white" or "black"! Good time to use imshow :D')

    array_data = img.copy()

    # Mask the array
    array_data[np.where(mask == 0)] = color_val

    # Check the array data format
    if len(np.shape(array_data)) > 2 and np.shape(array_data)[-1] > 3:
        # Replace this part with _make_pseudo_rgb
        num_bands = np.shape(array_data)[2]
        med_band = int(num_bands / 2)
        debug = params.debug
        params.debug = None
        pseudo_rgb = cv2.merge((rescale(array_data[:, :, 0]),
                                rescale(array_data[:, :, med_band]),
                                rescale(array_data[:, :, num_bands - 1])))
        params.debug = debug

        if params.debug == 'print':
            print_image(pseudo_rgb, os.path.join(params.debug_outdir, str(params.device) + '_masked.png'))
        elif params.debug == 'plot':
            plot_image(pseudo_rgb)
    else:
        if params.debug == 'print':
            print_image(array_data, os.path.join(params.debug_outdir, str(params.device) + '_masked.png'))
        elif params.debug == 'plot':
            plot_image(array_data)

    return array_data
