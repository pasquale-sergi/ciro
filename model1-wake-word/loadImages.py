import cv2
import numpy as np

#we load the images modelling size, dimensionality, pixel scale in order
#to prepare the data for the CNN

def loadImages(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img=cv2.resize(img, (128,128))
        img = img/255.0
        images.append(img)
    images = np.array(images)
    images = np.expand_dims(images, axis=-1)
    return images