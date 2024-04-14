from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import os
import time

import socket

# Create your views here.

def index(request):
    messages = {}
    if(request.method == 'POST'):
        print("POST request received")
        # implement image receiving and processing here
        # check if the request has a image in the form
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            if isinstance(image_file, InMemoryUploadedFile):

                # convert the image_file to jpeg format
                image_file = Image.open(image_file)

                print("Image file received")
                temp_dir = './static/.tmp/'
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Generate a timestamp for the image file name
                timestamp = str(int(time.time()))

                # Save the image file with the timestamp as the file name
                image_path = f'{temp_dir}{timestamp}.jpeg'
                image_file.save(image_path, 'JPEG')

                # Create a UDP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # send the image file path to the server
                sock.sendto(os.path.abspath(image_path).encode(), ('localhost', 12345))
                # wait to receive the response
                _, _ = sock.recvfrom(1024)
                # close the socket
                sock.close()

                matched_images_dir = image_path.split('.jpeg')[0] + '_matched/'

                
                messages['matched_images'] = []
                for img in os.listdir(matched_images_dir):
                    messages['matched_images'].append(f'{matched_images_dir}{img}')
                messages['image'] = image_path
                #

                # pass
            else:
                messages['error'] = 'Invalid image file'
        else:
            messages['error'] = 'No image file found'
    return render(request, 'index.html', messages)