# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:35:52 2025

@author: NP
"""
# pip install deepface
# pip install retina-face
from retinaface import RetinaFace
from deepface import DeepFace
import numpy as np
import cv2
import time
import os
import json
import redis
import threading
from glob import glob
from tqdm import tqdm
import random


images_directory = "./data"
save_path = "./result"
valid_images = ["*.jpg","*.png","*.jpeg"]

# create a Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# create save directory
if os.path.isdir(save_path) is False:
    os.mkdir(save_path)


def landmarks (images_directory, valid_images):
    start = time.time()
    # List of file names
    filenames = [f for ext in valid_images for f in glob(os.path.join(images_directory, ext))]  
    # shuffle filenames list
    random.shuffle(filenames)
    for img_path in tqdm(filenames, ncols=100, desc="Facial Landmarks"):
        # using basename function for file name
        basename = os.path.basename(img_path).split('/')[-1]
        file_name, file_extension = os.path.splitext(basename)
        # get facial landmarks from RetinaFace
        faces = RetinaFace.detect_faces(img_path)
        # Time = {"process":{"value":(time.time()-start) * 10**3, "string":f"{(time.time()-start) * 10**3:.2f}:ms"}}
        faces["Time_landmark"] = f"{(time.time()-start) * 10**3:.2f}:ms"
        # save facial landmarks to redis
        r.hset(file_name, "LANDMARKS", str(faces))
        # Store all attributes when they are provided completely
        if r.hget(file_name, "ANALYZE") is not None:
            # conver bytes to str
            dictionary = r.hgetall(file_name)
            converted_dict = {key.decode(): value.decode() for key, value in dictionary.items()}
            # save collected data as a JSON fle
            with open(f"{save_path}/{file_name}.json", "w") as outfile:
                json.dump(converted_dict, outfile)
            # remove completed file from Redis
            r.delete(file_name)
    # print("completed Facial Landmarks")    
      

def analyze (images_directory, valid_images):
    start = time.time()
    # List of file names
    filenames = [f for ext in valid_images for f in glob(os.path.join(images_directory, ext))]  
    # shuffle filenames list
    random.shuffle(filenames)
    for img_path in tqdm(filenames, ncols=100, desc="Age/Gender Estimation"):
        # using basename function for file name
        basename = os.path.basename(img_path).split('/')[-1]
        file_name, file_extension = os.path.splitext(basename)
        # Age/Gender Estimation from DeepFace
        analyze = DeepFace.analyze(img_path = img_path, actions = ['age', 'gender'], silent = True)
        analyze = dict(enumerate(analyze,1))
        analyze["Time_analyze"] = f"{(time.time()-start) * 10**3:.2f}:ms"
        # save Age/Gender Estimation to redis
        r.hset(file_name, "ANALYZE", str(analyze))
        # Store all attributes when they are provided completely
        if r.hget(file_name, "LANDMARKS") is not None:
            # conver bytes to str
            dictionary = r.hgetall(file_name)
            converted_dict = {key.decode(): value.decode() for key, value in dictionary.items()}
            # save collected data as a JSON fle
            with open(f"{save_path}/{file_name}.json", "w") as outfile:
                json.dump(converted_dict, outfile)
            # remove completed file from Redis
            r.delete(file_name)
    # print("completed Age/Gender Estimation")

# landmarks (images_directory, valid_images)
# analyze (images_directory, valid_images)

#################################### threads ######################################################
thread1 = threading.Thread(target=landmarks, args=[images_directory, valid_images], daemon=True) 
thread2 = threading.Thread(target=analyze, args=[images_directory, valid_images], daemon=True) 

# Start the threads
thread1.start()
thread2.start()
print("completed all attributes")
# tracker_thread1.join()
# tracker_thread2.join()
