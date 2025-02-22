import tkinter as tk
import numpy as np
import cv2 as cv
from PIL import Image, ImageTk
import display
import timeit

print(chr(97))

exit(0)

def change_channel(value, img):
    print(value)
    modified_img = img.copy()
    modified_img[:, :, :] = value 
    img_rgb = cv.cvtColor(modified_img, cv.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)    
    label.config(image=img_tk)
    label.image = img_tk

def on_slider_move(value):
    change_channel(value, curr_img)

# Create the main window
root = tk.Tk()
root.title("Slider Example")
blank_image = np.zeros((512,512,3), np.uint8)
img_tk = display.convertCvToTk(blank_image)
# Create a label to display slider value
label = tk.Label(root, image=img_tk)
curr_img = blank_image
label.pack()
# Create a slider widget
slider = tk.Scale(root, from_=0, to=255, orient="horizontal", command=on_slider_move)
slider.pack()

# Start the Tkinter event loop
root.mainloop()