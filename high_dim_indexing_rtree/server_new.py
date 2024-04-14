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
limit = 1500


# load mappings from the csv file
global_mappings = {}   
df = pd.read_csv('mapping_new.csv')
for idx, row in df.iterrows():
    global_mappings[row['index']] = row['filename']
df = None



features = np.load('features_new.npy')
dim = features.shape[1]

p = index.Property()
p.dimension = dim


# Create the rtree index for dim-dimensional data
idx = index.Index(properties=p)


mappings = {}
    
match_count = 5
def get_matched_images(query_vector):
    nearest = list(idx.nearest(tuple(query_vector), match_count))
    matched_imgs = []
    for i in range(match_count):
        print(nearest[i])
        matched_imgs.append(IMAGES_DIR+mappings[nearest[i]])
    return matched_imgs
    


# initialise the feature extractor
obj = FeatureExtractor()

    

# randomly select some indexes from 1 to len(features)
import random
indexes = random.sample(range(0, len(features)), limit)

count = 0

for i in indexes:
    count+=1
    img_features = features[i]
    idx.insert(count, tuple(img_features))
    mappings[count] = global_mappings[i]


print("Images inserted successfully!")

print('Setting up the server...')

import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to an address and port
server_socket.bind(('localhost', 12345))
print("Server is listening...")

# Receive data from the client

while True:
    data, address = server_socket.recvfrom(1024)
    print(f"Received data from {address}: {data}")
    if data.decode() == 'exit':
        break
    file_path = data.decode()
    img = Image.open(file_path)
    img_features = obj.extract_features(np.array(img))
    
    
    print("Query image: ", file_path)
    matched_imgs = get_matched_images(img_features)
    
    # copy those images and store the in directory of the file_path
    # remove the .jpeg from file_path and make a new dir
    new_dir = file_path.split('.jpeg')[0]+'_matched/'
    print('Saving images in ', new_dir)
    os.mkdir(new_dir)

    for i in range(match_count):
        img = Image.open(matched_imgs[i])
        img.save(new_dir+'/'+str(i)+'.jpeg')
    
    # send something for the client to know that the images are saved
    server_socket.sendto("Images saved!".encode(), address)

