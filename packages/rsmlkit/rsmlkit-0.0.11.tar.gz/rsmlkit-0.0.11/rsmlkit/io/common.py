#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: common.py
# Author: Raeid Saqur
# Email: raeidsaqur@cs.toronto.edu
# Created on: 08/07/2020
#
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import math
import contextlib
import os.path as osp

__all__ = ['auto_close', 'fsize_format', 'get_ext']

unit_list = list(zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2]))

@contextlib.contextmanager
def auto_close(file):
    yield file
    file.close()

def fsize_format(num):
    """Human readable file size."""
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

    exponent = min(int(math.log(num, 1024)), len(unit_list) - 1)
    quotient = float(num) / 1024**exponent
    unit, num_decimals = unit_list[exponent]
    format_string = '{:.%sf} {}' % num_decimals
    return format_string.format(quotient, unit)


def get_ext(fname, match_first=False):
    if match_first:
        fname = osp.split(fname)[1]
        return fname[fname.find('.'):]
    else:
        return osp.splitext(fname)[1]