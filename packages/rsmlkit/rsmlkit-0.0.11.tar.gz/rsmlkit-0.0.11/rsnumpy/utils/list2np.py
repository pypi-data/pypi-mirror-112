#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: list2np.py
# Author: Raeid Saqur
# Email: rsaqur@cs.princeton.edu
# Created on: 13/04/2019
#
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import numpy as np

from rsmlkit.logging import get_logger, set_default_level, log_dash
logger = get_logger(__file__)

__all__ = ['vectorize2DList', 'vectorize3DList']

# 2d list to numpy
def vectorize2DList(items, minX = 0, minY = 0, dtype = np.int):
    maxX = max(len(items), minX)
    maxY = max([len(item) for item in items] + [minY])
    t = np.zeros((maxX, maxY), dtype = dtype)
    tLengths = np.zeros((maxX, ), dtype = np.int)
    for i, item in enumerate(items):
        t[i, 0:len(item)] = np.array(item, dtype = dtype)
        tLengths[i] = len(item)
    return t, tLengths

# 3d list to numpy
def vectorize3DList(items, minX = 0, minY = 0, minZ = 0, dtype = np.int):
    maxX = max(len(items), minX)
    maxY = max([len(item) for item in items] + [minY])
    maxZ = max([len(subitem) for item in items for subitem in item] + [minZ])
    t = np.zeros((maxX, maxY, maxZ), dtype = dtype)
    tLengths = np.zeros((maxX, maxY), dtype = np.int)
    for i, item in enumerate(items):
        for j, subitem in enumerate(item):
            t[i, j, 0:len(subitem)] = np.array(subitem, dtype = dtype)
            tLengths[i, j] = len(subitem)
    return t, tLengths

