#!/bin/python

import os
import struct
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt

save_root = './.tmpimg/'
os.makedirs(save_root, exist_ok=True)


def read_bmeii_im(bmeii_file):
    with open(bmeii_file, 'rb') as f:
        file_name = os.path.basename(bmeii_file).replace('.bmeii', '')
        save_path = os.path.join(save_root, file_name + '.png')

        try:
            rows = struct.unpack('I', f.read(4))[0]
            cols = struct.unpack('I', f.read(4))[0]
            slcs = struct.unpack('I', f.read(4))[0]

            px_spac_x = struct.unpack('f', f.read(4))[0]
            px_spac_y = struct.unpack('f', f.read(4))[0]
            slc_thick = struct.unpack('f', f.read(4))[0]

            raw_im = f.read(rows * cols * slcs * 8)
            image_array = np.array(
                struct.unpack('h' * rows * cols * slcs, raw_im))
            image_array = image_array.reshape((rows, cols))

            # Saves as RGBA
            plt.imsave(save_path, image_array, cmap='bone')
            return save_path

        except KeyboardInterrupt as e:
            print('Skipping', bmeii_file, e.args)


def loader(image_list):
    loader_pool = multiprocessing.Pool(4)
    saved_images = loader_pool.map(read_bmeii_im, image_list)
    loader_pool.close()
    loader_pool.join()

    return saved_images
