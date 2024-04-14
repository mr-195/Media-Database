# Media-Database
Media database as a part of term project for DBMS course.

# How to run
1. Run server.py file present in ./high_dim_indexing_rtree (cd high_dim_indexing_rtree; python3 server.py)
2. Run django backend to create a web interface (cd backend/dbms; python3 manage.py runserver)
3. Open the Web page in the browser to use the application

Note:
1. Run server_new.py to use updated dataset that contains images of vehicles along with images of animals from the previous dataset.


-- Changes from previous commit
Train data from vehicles dataset from kaggle is added to images folder.
Vehicle data is separately stored at Images_vehicles.
Animals data is separately stored at Images_animals.
New server(server_new.py) and feature_extractor(image_2_features.py) and realtime tester (test_new.py) and mappings for updated images (mapping_new.csv) are added.
All these new files are added to high_dim_indexing_rtree

