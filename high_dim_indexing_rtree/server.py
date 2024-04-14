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

#load the data
points = np.load('Data/features.npy')
img_files = pd.read_csv('Data/mapping.csv')
insert_count = 100
dim = points.shape[2]   ##
print(f'Dimension: {dim}')

p = index.Property()
p.dimension = dim


# Create the rtree index for dim-dimensional data
idx = index.Index(properties=p)


# Insert some points into the index
for i in tqdm(range(insert_count)):
    idx.insert(i, tuple(points[i][0]))
    
match_count = 5
def get_matched_images(query_vector):
    nearest = list(idx.nearest(tuple(query_vector), match_count))
    matched_imgs = []
    for i in range(match_count):
        matched_imgs.append(IMAGES_DIR+img_files.iloc[nearest[i]]['filename'])
    return matched_imgs
    
# initialise the feature extractor
obj = FeatureExtractor()


    






import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to an address and port
server_socket.bind(('localhost', 12345))

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
