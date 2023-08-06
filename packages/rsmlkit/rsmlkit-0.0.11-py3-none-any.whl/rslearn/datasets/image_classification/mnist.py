#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File: mnist.py
# Author: raeidsaqur
# Email: rsaqur@cs.princeton.edu
# Created on: 2021-07-08
# 
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import os.path as osp
import gzip
import pickle

from rsmlkit.io.network import download

__all__ = ['load_mnist']

def load_mnist(
    data_dir,
    data_file='mnist.pkl.gz',
    origin='http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'):

    dataset = osp.join(data_dir, data_file)

    if (not osp.isfile(dataset)) and data_file == 'mnist.pkl.gz':
        download(origin, data_dir, data_file)

    # Load the dataset
    with gzip.open(dataset, 'rb') as f:
        try:
            train_set, valid_set, test_set = pickle.load(f, encoding='latin1')
        except:
            train_set, valid_set, test_set = pickle.load(f)
    return train_set, valid_set, test_set