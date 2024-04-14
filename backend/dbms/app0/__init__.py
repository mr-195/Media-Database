# #how to use a package that is another directory
# import os
# import sys

# BASE_DIR = '../../high_dim_indexing_rtree/'

# print("Hello World")
# print(os.path.abspath(BASE_DIR))

# sys.path.append(os.path.abspath('../../high_dim_indexing_rtree/'))

# from Model.rtree import index
# from image_viewer import ImageViewer
# import numpy as np
# import pandas as pd
# from tqdm import tqdm


# from Model.featureExtractor import FeatureExtractor
# a

# # Constants
# IMAGES_DIR = BASE_DIR + 'Data/Images/'
# POINTS_DIR = BASE_DIR + 'Data/features.npy'
# MAPPING_DIR = BASE_DIR + 'Data/mapping.csv'

# #load the data
# points = np.load(POINTS_DIR)
# img_files = pd.read_csv(MAPPING_DIR)
# insert_count = 100
# dim = points.shape[2]   ##
# print(f'Dimension: {dim}')

# p = index.Property()
# p.dimension = dim


# # Create the rtree index for dim-dimensional data
# idx = index.Index(properties=p)


# # Insert some points into the index
# for i in tqdm(range(insert_count)):
#     idx.insert(i, tuple(points[i][0]))
    
# match_count = 4
# def get_matched_images(query_vector):
#     nearest = list(idx.nearest(tuple(query_vector), match_count))
#     matched_imgs = []
#     for i in range(match_count):
#         matched_imgs.append(IMAGES_DIR+img_files.iloc[nearest[i]]['filename'])
#     return matched_imgs
    
# # initialise the feature extractor
# obj = FeatureExtractor()


    
# # # Find the M nearest point to a given point
# M = 4
