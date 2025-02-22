import cv2 as cv
from cv2.typing import MatLike
import numpy as np
#poc6
def median_filter(img: MatLike) -> MatLike:
    height, width, channels = img.shape
    
    filtered_image = np.zeros((height, width, channels), dtype=np.uint8)
    
    for c in range(channels):
        for i in range(1, height-1):
            for j in range(1, width-1):
                neighborhood = [
                    img[i-1, j-1, c], img[i-1, j, c], img[i-1, j+1, c],
                    img[i, j-1, c], img[i, j, c], img[i, j+1, c],
                    img[i+1, j-1, c], img[i+1, j, c], img[i+1, j+1, c]
                ]

                median_value = np.median(neighborhood)
                filtered_image[i, j, c] = median_value
    
    return filtered_image

def max_filter(img: MatLike) -> MatLike:
    height, width, channels = img.shape
    
    filtered_image = np.zeros((height, width, channels), dtype=np.uint8)
    
    for c in range(channels):
        for i in range(1, height-1):
            for j in range(1, width-1):
                neighborhood = [
                    img[i-1, j-1, c], img[i-1, j, c], img[i-1, j+1, c],
                    img[i, j-1, c], img[i, j, c], img[i, j+1, c],
                    img[i+1, j-1, c], img[i+1, j, c], img[i+1, j+1, c]
                ]

                max_value = np.max(neighborhood)
                filtered_image[i, j, c] = max_value
    
    return filtered_image

def min_filter(img: MatLike) -> MatLike:
    height, width, channels = img.shape
    
    filtered_image = np.zeros((height, width, channels), dtype=np.uint8)
    
    for c in range(channels):
        for i in range(1, height-1):
            for j in range(1, width-1):
                neighborhood = [
                    img[i-1, j-1, c], img[i-1, j, c], img[i-1, j+1, c],
                    img[i, j-1, c], img[i, j, c], img[i, j+1, c],
                    img[i+1, j-1, c], img[i+1, j, c], img[i+1, j+1, c]
                ]

                min_value = np.min(neighborhood)
                filtered_image[i, j, c] = min_value
    
    return filtered_image
