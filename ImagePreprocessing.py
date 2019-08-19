import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import glob
import os
import re
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

fileDirectory = r'.\Datasets\phase-01\data\sentinel-2a-tile-7680x-10240y\timeseries'
arr = os.listdir(fileDirectory)


def imagestack_npConvert(band, fileDir):
    emissionBand = [x for x in arr if re.search('-'+band+'-', x)]
    emissionBand = [fileDirectory + '\\' + s for s in emissionBand]
    images = [Image.open(i) for i in emissionBand]
    
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    if band[0] == 'B':
        new_img = Image.new('I', (total_width, max_height))
    else:
        new_img = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_img.paste(im, (x_offset,0))
        x_offset += im.size[0]
        
    return np.array(new_img)

def normaliseToImage(imageArray):
    imageArrayNorm = (vegIndex - vegIndex.min())/(vegIndex.max() - vegIndex.min())
    imageArrayNorm = Image.fromarray(np.uint8(imageArrayNorm*255))
    return imageArrayNorm

        

####################
# Vegetation Index #
####################  
vegIndex = (imagestack_npConvert('B08', fileDirectory) - imagestack_npConvert('B04', fileDirectory))/(imagestack_npConvert('B08', fileDirectory) + imagestack_npConvert('B04', fileDirectory))

normaliseToImage(vegIndex).save('vegationIndex.png')

##################
# Moisture Index #
##################
moistureIndex = (imagestack_npConvert('B8A', fileDirectory) - imagestack_npConvert('B11', fileDirectory))/(imagestack_npConvert('B8A', fileDirectory) + imagestack_npConvert('B11', fileDirectory))

normaliseToImage(moistureIndex).save('MoistureIndex.png')
