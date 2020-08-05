#!/bin/python

import os
import struct
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt

from config import Config


def read_bmeii_im(bmeii_file):
    file_name = os.path.basename(bmeii_file).replace('.bmeii', '')
    save_path = os.path.join(Config.save_root, file_name + '.png')

    with open(bmeii_file, 'rb') as f:
        try:
            rows = struct.unpack('I', f.read(4))[0]
            cols = struct.unpack('I', f.read(4))[0]
            slcs = struct.unpack('I', f.read(4))[0]

            # These lines are required even if the vairables aren't read
            px_spac_x = struct.unpack('f', f.read(4))[0]
            px_spac_y = struct.unpack('f', f.read(4))[0]
            slc_thick = struct.unpack('f', f.read(4))[0]

            raw_im = f.read(rows * cols * slcs * 8)
            image_array = np.array(
                struct.unpack('h' * rows * cols * slcs, raw_im))
            image_array = image_array.reshape((rows, cols))

            # Saves as RGBA
            plt.imsave(save_path, image_array, cmap=Config.cmap)
            return save_path

        except KeyboardInterrupt as e:
            print('Skipping', bmeii_file, e.args)


def loader(image_list):
    # Clear the image cache
    for i in os.listdir(Config.save_root):
        os.remove(os.path.join(Config.save_root, i))

    loader_pool = multiprocessing.Pool(4)
    saved_images = loader_pool.map(read_bmeii_im, image_list)
    loader_pool.close()
    loader_pool.join()

    return saved_images
