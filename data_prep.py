# This script fetches the Gbongan imagery, preps it, and outputs.
import numpy as np
import pandas as pd
import keras
from PIL import Image
from scipy import ndimage
import matplotlib.pyplot as plt

# Normalize matrix
def norm(mat):
    mat_max = mat.max()
    mat_min = mat.min()
    new_mat = (mat - mat_min) / (mat_max - mat_min)
    return new_mat

# Imports images as normalized NP
def image_import(path, band, ftype = '.npy'):
    full_path = path + band + ftype
    if ftype == '.npy':
        im = np.load((full_path))
    else:
        im = Image.open(full_path)
        im = np.array(im)[:,:,0]
    return norm(im)

# Calculates ndvi
def prep_ndvi(red, ir):
    ndvi = np.true_divide((ir - red), (ir + red))
    return ndvi

# Stack bldg + ndvi. If BUILDING (1), make it NAN. Else, keep NVDVI value.
def prep_output(red, ir):
    ndvi = prep_ndvi(red, ir)
    output = ndvi.reshape(ndvi.shape[0]*ndvi.shape[1]) # Flatten matrix
    output[output < -0.05] = np.nan # Thresholds for buildings; sets to
    output = output.reshape(ndvi.shape)
    return output

# Full run commands:
def main():
    path = 'data/Gbongan/JPGs/'
    red = image_import(path, 'red', '.jpg')
    ir = image_import(path, 'IR', '.jpg')
    output = prep_output(red, ir)
    np.save('data/output.npy', output)
