import cv2 as cv
from cv2.typing import MatLike
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np
#kanaly
#poc2

def oneChannel(img: MatLike, color: str):
    match color:
        case "red": 
            img[:,:,1] = 0
            img[:,:,2] = 0
        case "green":
            img[:,:,0] = 0
            img[:,:,2] = 0
        case "blue":
            img[:,:,0] = 0
            img[:,:,1] = 0
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    cv.imshow(color, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def change_channel(root, value, img: MatLike, color):
    modified_img = img.copy()
    match color:
        case "red":
            modified_img[:, :, 0] = value
        case "green":
            modified_img[:, :, 1] = value
        case "blue":
            modified_img[:, :, 2] = value
    root.set_curr_img(modified_img)

#slicing

def RGB_to_HSV(img: MatLike) -> MatLike:
    hsv_img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    return hsv_img

def RGB_to_YUV(img: MatLike) -> MatLike:
    yuv_img = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    return yuv_img

def RGB_to_YUV_mine(img: MatLike) -> MatLike:
    height, width, *rest = img.shape
    new_img = np.zeros_like(img, np.float32)
    for i in range(0, width):
        for j in range(0, height):
            r, g, b = new_img[j, i]
            new_img[j, i, 0] = 0.299 * r + 0.587 * g + 0.114 * b
            new_img[j, i, 1] = 0.492 * (b - img[j, i, 0])
            new_img[j, i, 2] = 0.877 * (r - img[j, i, 0])

#slicing

def color_to_black_and_white1(img: MatLike) -> MatLike:
    gr_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    return gr_img
    
def color_to_black_and_white2(img: MatLike) -> MatLike:
    height, width, *rest = img.shape
    gr_img = np.copy(img)
    for i in range(0, width):
        for j in range(0, height):
            sum = 0
            sum += gr_img[j, i, 0]
            sum += gr_img[j, i, 1]
            sum += gr_img[j, i, 2]
            gr_img[j, i, :] = sum/3

    #slicing
    return gr_img

def color_to_black_and_white3(img: MatLike) -> MatLike:

    new_img = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    print(new_img)
    return new_img

def grey_histogram(img: MatLike) -> int:
    width, height, *rest = img.shape
    histogram = np.zeros(256, dtype=int)
    for i in range(0, width):
            for j in range(0, height):
                intensity = img[i, j]
                histogram[intensity] += 1

    #slicing
    histogram[0] = 0
    plt.bar(range(256), histogram, color='black')
    plt.title('Grayscale Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.show()

def grey_histogram_fun(img: MatLike, show: bool) -> int:
    hist = cv.calcHist([img], [0], None, [256], [0, 256])
    maxY = np.argmax(hist)
    if show:
        plt.plot(hist, color='gray')
        plt.xlabel('Odcień szarości')
        plt.ylabel('Liczebność pikseli')
        plt.title('Histogram odcieni szarości')
        plt.show()
    return maxY

def rgb_histogram(img: MatLike):
    hist_R = cv.calcHist([img], [0], None, [256], [0,256])
    hist_G = cv.calcHist([img], [1], None, [256], [0,256])
    hist_B = cv.calcHist([img], [2], None, [256], [0,256])

    plt.plot(hist_R, color='red')
    plt.plot(hist_G, color='green')
    plt.plot(hist_B, color='blue')
    plt.xlabel('Kanaly')
    plt.ylabel('Liczebność pikseli')
    plt.title('Histogram RGB')
    plt.show()
        
