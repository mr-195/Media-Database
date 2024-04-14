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

#load the data
points = np.load('Data/features.npy')
img_files = pd.read_csv('Data/mapping.csv')
insert_count = 7000
dim = points.shape[2]   ##
print(f'Dimension: {dim}')

p = index.Property()
p.dimension = dim


# Create the rtree index for dim-dimensional data
idx = index.Index(properties=p)


# Insert some points into the index
# for i in tqdm(range(insert_count)):
#     idx.insert(i, tuple(points[i][0]))
    
match_count = 1
def get_matched_images(query_vector):
    nearest = list(idx.nearest(tuple(query_vector), match_count))
    matched_imgs = []
    for i in range(match_count):
        print(nearest[i])
        matched_imgs.append(IMAGES_DIR+img_files.iloc[nearest[i]]['filename'])
    return matched_imgs
    
# initialise the feature extractor
obj = FeatureExtractor()

limit = CURRENT_LIMIT
count = 0
mappings = {}
images = []


for image in os.listdir(IMAGES_DIR):
    images.append(image)

# randomly select images and insert them into the index
import random
random.shuffle(images)



for image in images:
    if count == limit:
        break
    count+=1
    print(image)
    # obj = FeatureExtractor()
    try:
        img = Image.open(IMAGES_DIR+image)
        img_features = obj.extract_features(np.array(img))
        idx.insert(count, tuple(img_features))
        mappings[count] = image
    except:
        print("Error in extracting features from image")
        continue
    # np.append(points, img_features)

print("Image inserted successfully!")

# limit = CURRENT_LIMIT
# count = 0

# for image in os.listdir(IMAGES_DIR):
#     if count == limit:
#         break
#     count+=1
#     img = Image.open(IMAGES_DIR+image)
#     img_features = obj.extract_features(np.array(img))
#     nearest = list(idx.nearest(tuple(img_features), 1)) 
#     print(image,"=>",nearest)
    

def func(choice):
    try:
        img = Image.open('/home/thota/Desktop/dump/' + choice)
    except:
        print("Invalid image name")
        return
    img_features = obj.extract_features(np.array(img))
    
    nearest = list(idx.nearest(tuple(img_features), 10))
    for i in range(10):
        print(nearest[i], "=>", mappings[nearest[i]])

while(1):
    choice = input("Enter the image name: ")
    if choice == 'exit':
        break
    func(choice)



