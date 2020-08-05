#!/bin/python

import os


class Config:
    cmaps = {}

    cmaps['Perceptually Uniform Sequential'] = [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis']

    cmaps['Sequential'] = [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    cmaps['Sequential (2)'] = [
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']

    cmaps['Sequential (2)'] = [
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']

    cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

    cmaps['Qualitative'] = [
        'Pastel1', 'Pastel2', 'Paired', 'Accent',
        'Dark2', 'Set1', 'Set2', 'Set3',
        'tab10', 'tab20', 'tab20b', 'tab20c']

    cmaps['Miscellaneous'] = [
        'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
        'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
        'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']


    # Save temporary images here
    save_root = './.tmpimg/'
    os.makedirs(save_root, exist_ok=True)

    # For the sake of multiprocessing
    cmap = 'bone'
