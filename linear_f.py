import cv2 as cv
from cv2.typing import MatLike
import numpy as np
#poc5
def linear_filter(img: MatLike, mask: np.array) -> MatLike:
    height, width, channels = img.shape
    
    filtered_image = np.zeros((height, width, channels), dtype=np.uint8)
    
    for c in range(channels):
        for i in range(1, height-1):
            for j in range(1, width-1):
                sum_value = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        sum_value += mask[k+1, l+1] * img[i+k, j+l, c]
                
                sum_value = np.clip(sum_value, 0, 255)
                filtered_image[i, j, c] = sum_value
    
    return filtered_image