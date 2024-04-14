import numpy as np
import pandas as pd
from tqdm import tqdm
from PIL import Image, ImageTk
from random import random
import tkinter as tk
from tkinter import filedialog
import os

from Model.rtree import index
from image_viewer import ImageViewer


from Model.featureExtractor import FeatureExtractor


# Constants
IMAGES_DIR = 'Data/Images/'
CURRENT_LIMIT = 1500
limit = CURRENT_LIMIT
count = 0
mappings = {}
images = []

obj = FeatureExtractor()

features = []
i = 0

for image in os.listdir(IMAGES_DIR):
    print(image)
    try:
        features.append(obj.extract_features(np.array(Image.open(IMAGES_DIR+image))))
        mappings[i] = image
        # print(image)
        i += 1
    except:
        pass

# convert the features to numpy array
features = np.array(features)
# save the features to a file
np.save('features_new.npy', features)

# save mappings into a csv file
df = pd.DataFrame(mappings.items(), columns=['index', 'filename'])
df.to_csv('mapping_new.csv', index=False)