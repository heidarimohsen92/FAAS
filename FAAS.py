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

# # Read and display an image
# image = cv2.imread('data/MultipleFaces.jpg')
# cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
# cv2.imshow('Image', image)
# # Wait for a key press and close the window
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img_path = "data/MultipleFaces2.jpg"
def landmarks (img_path):
    start = time.time()
    faces = RetinaFace.detect_faces(img_path)
    Time = {"process":{"value":(time.time()-start) * 10**3, "string":f"{(time.time()-start) * 10**3:.2f}:ms"}}
    faces["Time_landmark"] = Time
    print(faces)

def analyze (img_path):
    start = time.time()
    analyze = DeepFace.analyze(img_path = img_path, actions = ['age', 'gender'])
    analyze = dict(enumerate(analyze,1))
    Time = {"process":{"value":(time.time()-start) * 10**3, "string":f"{(time.time()-start) * 10**3:.2f}:ms"}}
    analyze["Time_analyze"] = Time
    print(analyze)

landmarks (img_path)
analyze (img_path)