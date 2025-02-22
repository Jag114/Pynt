#poc4
import cv2 as cv
import numpy as np
from cv2.typing import MatLike
import colors

def compare_image(img: MatLike, img2: MatLike):
    width, height, *rest = img.shape
    img2 = cv.resize(img2, (width, height))
    gray_img = colors.color_to_black_and_white1(img) 
    gray_img2 = colors.color_to_black_and_white1(img2)
    new_img = np.zeros_like(img, np.uint8)
    for i in range(0, width):
        for j in range(0, height):
            curr_pixel_diff = gray_img[j, i] - gray_img2[j, i]
            if curr_pixel_diff > 0:
                new_img[j, i] = curr_pixel_diff
            else:
                new_img[j, i] = 0

    cv.imshow("Image 1", gray_img)
    cv.imshow("Image 2", gray_img2)
    cv.imshow("Image 3", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def horizontal_edges(img: MatLike):
    print("Poziome")
    width, height, *rest = img.shape
    moved_img = img.copy()
    translation_matrix = np.float32([[1, 0, 0], [0, 1, 1]])
    moved_img = cv.warpAffine(moved_img, translation_matrix, (height, width))
    moved_img[:, :] = np.abs(moved_img[:, :] - img[:, :])

    cv.imshow("Image edges", moved_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def vertical_edges(img: MatLike):
    print("Pionowe")
    width, height, *rest = img.shape
    moved_img = img.copy()
    translation_matrix = np.float32([[1, 0, 1], [0, 1, 0]])
    moved_img = cv.warpAffine(moved_img, translation_matrix, (height, width))
    moved_img[:, :] = np.abs(moved_img[:, :] - img[:, :])

    cv.imshow("Image edges", moved_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def beveled_edges(img: MatLike):
    print("Ukosne")
    width, height, *rest = img.shape
    moved_img = img.copy()
    translation_matrix_x = np.float32([[1, 0, 1], [0, 1, 0]])
    translation_matrix_y = np.float32([[1, 0, 0], [0, 1, 1]])
    moved_img = cv.warpAffine(moved_img, translation_matrix_x, (height, width))
    moved_img = cv.warpAffine(moved_img, translation_matrix_y, (height, width))
    moved_img[:, :] = np.abs(moved_img[:, :] - img[:, :])

    cv.imshow("Image edges", moved_img)
    cv.waitKey(0)
    cv.destroyAllWindows()