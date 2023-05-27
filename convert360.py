#!/usr/bin/env python

import argparse
import numpy as np
from PIL import Image

import py360convert

# написать это как класс Convert

def SaveEquiToCubic_convert(file_path, height, new_name_file):
    img = np.array(Image.open(file_path))
    if len(img.shape) == 2:
        img = img[..., None]
    out = py360convert.e2c(img, face_w=height, mode="bilinear")
    Image.fromarray(out.astype(np.uint8)).save(new_name_file)

def SaveCubicToEqui_convert(file_path, new_name_file, width, height):
    img = np.array(Image.open(file_path))
    if len(img.shape) == 2:
        img = img[..., None]
    out = py360convert.c2e(img, h=height, w=width, mode="bilinear")
    Image.fromarray(out.astype(np.uint8)).save(new_name_file)
