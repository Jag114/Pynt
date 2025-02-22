import cv2 as cv
import numpy as np
from cv2.typing import MatLike
from PIL import ImageTk, Image #image conversion
    
def create_default(width: int, height: int ) -> MatLike:
    def_img = np.zeros((width, height, 3), np.uint8)
    def_img[:height//2, :width//2, :] = 128  # Top-left quadrant
    def_img[:height//2, width//2:, :] = (255, 0, 255)  # Top-right quadrant
    def_img[height//2:, :width//2, :] = (0, 255, 255)  # Bottom-left quadrant
    def_img[height//2:, width//2:, :] = (255, 255, 0)  # Bottom-right quadrant
    return def_img

# Funkcja do wczytania obrazu i konwersji do formatu zgodnego z Tkinter
def loadAndConvertImage(image_path: str) -> ImageTk:
    # Wczytaj obraz za pomocą OpenCV
    img_cv = cv.imread(image_path)
    # Konwertuj obraz do formatu RGB (potrzebnego dla Tkinter)
    img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)
    # Konwertuj obraz na obiekt Image z biblioteki PIL
    img_pil = Image.fromarray(img_rgb)
    # Skonwertuj obraz PIL na obiekt ImageTk, który jest kompatybilny z Tkinter
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk

def convertCvToTk(img_cv: MatLike) -> ImageTk:
    img_pil = Image.fromarray(img_cv)
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk

def display_image(img: MatLike):
    cv.imshow("", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

