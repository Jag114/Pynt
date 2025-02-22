from tkinter import * #GUI
from tkinter import filedialog
import display
import colors
import binary
import compare
import linear_f
import nonlinear_f
import cv2 as cv
from cv2.typing import MatLike
import numpy as np
import random

class Window:
    m_root: Tk
    m_label: Label
    m_menu_bar: Menu
    m_current_image: MatLike
    m_previous_image: MatLike
    m_current_image_width: int 
    m_current_image_height: int 

    def __init__(self):
        self.m_root = Tk()
        self.m_root.title("Pynt")
        self.m_root.iconbitmap("./images/pynt-icon.ico")
        self.m_root.geometry(f"{self.m_root.winfo_screenwidth()}x{self.m_root.winfo_screenheight()}")
        self.m_root.state('zoomed')
        self.m_root.resizable(True,True)

        self.m_label = Label(self.m_root)
        self.m_menu_bar = Menu(self.m_root)

        self.set_curr_img(display.create_default(768, 768))
        self.m_previous_image = None

        self.menu()

    def set_curr_img(self, new_img: MatLike):
        height, width, *rest = new_img.shape
        self.m_current_image_height = height
        self.m_current_image_width = width
        self.m_current_image = new_img
        img_tk = display.convertCvToTk(new_img)
        self.m_label.config(image=img_tk)
        self.m_label.image = img_tk

    #MENU
    def menu(self):
        self.m_root.config(menu=self.m_menu_bar)
        menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Options", menu=menu)
        colors_menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Colors", menu=colors_menu)
        binary_menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Binary", menu=binary_menu)
        compare_menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Compare", menu=compare_menu)
        linear_menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Filters", menu=linear_menu)

        menu_tab_names = ["New...", "Open...", "Save..."]
        menu_command_list = [self.create_file, self.open_file, self.save_file]

        colors_tab_names = ["1 channel", "Modify channel", "RGB to HSV", "RGB to YUV", "RGB to YUV (custom)",
                             "Greyscale 1", "Greyscale 2", "Greyscale 3", "Histogram", "RGB histogram"]
        colors_command_list = [self.one_channel, self.channel, self.RGB_to_HSV, self.RGB_to_YUV_mine, self.RGB_to_YUV, self.color_to_black_and_white1, 
                               self.color_to_black_and_white2, self.color_to_black_and_white3, self.grey_histogram, self.RGB_histogram]
        
        binary_tab_names = ["User thresholding", "Histogram thresholding", "Multi-thresholding"]
        binary_command_list = [self.threshold, self.threshold_histogram, self.threshold_multi]

        compare_tab_names = ["Compare images", "Horizontal edges", "Vertical edges", "Beveled edges"]
        compare_command_list = [self.compare_image, self.horizontal_edges, self.vertical_edges, self.beveled_edges]

        linear_tab_names = ["Enhance", "Blur", "Edge filter", "Horizontal edges", "Vertical edges", "Beveled edges 1", "Beveled edges 2"]
        linear_command_list = [self.up_filter, self.down_filter, self.horizontal_edge_filter, self.vertical_edge_filter,
                                self.beveled_edge_filter1, self.beveled_edge_filter2]
        
        nonlinear_tab_names = ["Median", "Max", "Min"]
        nonlinear_command_list = [self.median_filter, self.max_filter, self.min_filter]

        for tab_name, command in zip(menu_tab_names, menu_command_list):
            menu.add_command(label=tab_name, command=command)

        for tab_name, command in zip(colors_tab_names, colors_command_list):
            colors_menu.add_command(label=tab_name, command=command)

        for tab_name, command in zip(binary_tab_names, binary_command_list):
            binary_menu.add_command(label=tab_name, command=command)

        for tab_name, command in zip(compare_tab_names, compare_command_list):
            compare_menu.add_command(label=tab_name, command=command)

        for tab_name, command in zip(linear_tab_names, linear_command_list):
            linear_menu.add_command(label=tab_name, command=command)
        
        for tab_name, command in zip(nonlinear_tab_names, nonlinear_command_list):
            linear_menu.add_command(label=tab_name, command=command)

        label = self.m_label
        label.pack()

    #FILES
    def open_file(self, *args):
        if len(args) == 0:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
        else:
            file_path = args[0]

        if len(file_path) == 0:
            return

        #self.add_history(cv.imread(file_path))
        self.m_current_image = cv.imread(file_path)
        img_tk = display.loadAndConvertImage(file_path)
        self.m_label.config(image=img_tk)
        self.m_label.image = img_tk

    def create_file(self):
        new_file_window = Toplevel()
        new_file_window.title("Create New File")

        name_label = Label(new_file_window, text="Name:")
        name_entry = Entry(new_file_window)
        extension_label = Label(new_file_window, text="Extension:")
        extension_var = IntVar()
        jpg_radio = Radiobutton(new_file_window, text="JPG", variable=extension_var, value=1)
        png_radio = Radiobutton(new_file_window, text="PNG", variable=extension_var, value=2)
        width_label = Label(new_file_window, text="Width:")
        width_entry = Entry(new_file_window)
        height_label = Label(new_file_window, text="Height:")
        height_entry = Entry(new_file_window)

        # OK button to create the file
        def create_file_window():
            name = name_entry.get()
            extension = ".jpg" if extension_var.get() == 1 else ".png"
            width = int(width_entry.get())
            height = int(height_entry.get())
            blank_image = np.zeros((height,width,3), np.uint8)
            file_path = f"./images/{name}.{extension}"
            cv.imwrite(file_path, blank_image)
            self.m_current_image = cv.imread(file_path)
            self.open_file(file_path)
            new_file_window.destroy()

        ok_button = Button(new_file_window, text="OK", command=create_file_window)

        #Pack labels, entry fields, and OK button
        name_label.grid(row=0, column=0, sticky="e")
        name_entry.grid(row=0, column=1)
        extension_label.grid(row=1, column=0, sticky="e")
        jpg_radio.grid(row=1, column=1, sticky="w")
        png_radio.grid(row=1, column=1, sticky="e")
        width_label.grid(row=2, column=0, sticky="e")
        width_entry.grid(row=2, column=1)
        height_label.grid(row=3, column=0, sticky="e")
        height_entry.grid(row=3, column=1)
        ok_button.grid(row=4, columnspan=2)
    
    def save_file(self):
        name = ""
        #okno
        if name == "":
            random.seed(a=None)
            for i in range(0, 5):
                name += chr(int(random.uniform(97,122)))
                name += chr(int(random.uniform(65, 90)))
        cv.imwrite(f"./images/{name}.png", self.m_current_image)

    #COLORS
    def one_channel(self):
        colors.oneChannel(self.m_current_image.copy(), "red")
        colors.oneChannel(self.m_current_image.copy(), "green")
        colors.oneChannel(self.m_current_image.copy(), "blue")

    def channel(self):
        def on_slider_move(self, value, color: str):
            colors.change_channel(self, value, self.m_current_image, color)
        
        frame = Frame(self.m_root)
        frame_R = Frame(frame)
        frame_G = Frame(frame)
        frame_B = Frame(frame)

        label_R = Label(frame_R, text="Red Channel")
        label_G = Label(frame_G, text="Green Channel")
        label_B = Label(frame_B, text="Blue Channel")
        slider_R = Scale(frame_R, from_=0, to=255, orient="horizontal", command=lambda value: on_slider_move(self, value, "red"))
        slider_G = Scale(frame_G, from_=0, to=255, orient="horizontal", command=lambda value: on_slider_move(self, value, "green"))
        slider_B = Scale(frame_B, from_=0, to=255, orient="horizontal", command=lambda value: on_slider_move(self, value, "blue"))

        # Pack labels and sliders into their respective frames
        label_R.pack(side="left")
        slider_R.pack(side="right")
        label_G.pack(side="left")
        slider_G.pack(side="right")
        label_B.pack(side="left")
        slider_B.pack(side="right")

        done_button = Button(frame, text="Done", command=lambda: frame.destroy())
        done_button.pack(side="bottom", padx=20, pady=20)

        # Pack frames into the root window
        frame_R.pack(side="left")
        frame_G.pack(side="left")
        frame_B.pack(side="left")
        frame.pack(side="bottom", padx=10, pady=10)

    def RGB_to_HSV(self):
        new_img = colors.RGB_to_HSV(self.m_current_image)
        display.display_image(new_img)

    def RGB_to_YUV(self):
        new_img = colors.RGB_to_YUV(self.m_current_image)
        display.display_image(new_img)

    def RGB_to_YUV_mine(self):
        new_img = colors.RGB_to_YUV(self.m_current_image)
        display.display_image(new_img)

    def color_to_black_and_white1(self):        
        new_img = colors.color_to_black_and_white1(self.m_current_image)
        display.display_image(new_img)
    
    def color_to_black_and_white2(self):
        new_img = colors.color_to_black_and_white2(self.m_current_image)
        display.display_image(new_img)

    def color_to_black_and_white3(self):
        new_img = colors.color_to_black_and_white3(self.m_current_image)
        display.display_image(new_img)

    def grey_histogram(self):
        gray_img = self.m_current_image.copy()
        if self.m_current_image.shape == 3:
            gray_img = colors.color_to_black_and_white1(gray_img)
        colors.grey_histogram(gray_img)

    def RGB_histogram(self):
        colors.rgb_histogram(self.m_current_image)
 
    #BINARY
    def threshold(self):
        def get_values():
            min = int(min_entry.get())
            if len(self.m_current_image.shape) == 3:
                img_bin = cv.cvtColor(self.m_current_image.copy(), cv.COLOR_RGB2GRAY)
            img_bin = binary.threshold(img_bin, min)
            display.display_image(img_bin)
            pop_up.destroy()

        pop_up = Toplevel()
        min_label = Label(pop_up, text="Dolny prog:")
        min_entry = Entry(pop_up)
        accept = Button(pop_up, command=get_values, text="Done")
        min_label.grid(row=0, column=0)
        min_entry.grid(row=0, column=1)
        accept.grid(row=2, column=0)

    def threshold_histogram(self):
        if len(self.m_current_image.shape) == 3:
            img_bin = cv.cvtColor(self.m_current_image.copy(), cv.COLOR_RGB2GRAY)
        img_bin = binary.threshold(img_bin)
        display.display_image(img_bin)

    def threshold_multi(self):
        def get_values():
            min = int(min_entry.get())
            max = int(max_entry.get())
            if len(self.m_current_image.shape) == 3:
                img_bin = cv.cvtColor(self.m_current_image.copy(), cv.COLOR_RGB2GRAY)
            img_bin = binary.threshold(img_bin, min, max)
            display.display_image(img_bin)
            pop_up.destroy()

        pop_up = Toplevel()
        min_label = Label(pop_up, text="Dolny prog:")
        max_entry = Entry(pop_up)
        max_label = Label(pop_up, text="Gorny prog:")
        min_entry = Entry(pop_up)
        accept = Button(pop_up, command=get_values, text="Done")
        min_label.grid(row=0, column=0)
        min_entry.grid(row=0, column=1)
        max_label.grid(row=1, column=0)
        max_entry.grid(row=1, column=1)
        accept.grid(row=2, column=0)
        
    #COMPARE
    def compare_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
        compared_image = cv.imread(file_path)
        compare.compare_image(self.m_current_image, compared_image)

    #EDGES
    def horizontal_edges(self):
        compare.horizontal_edges(self.m_current_image)

    def vertical_edges(self):
        compare.vertical_edges(self.m_current_image)

    def beveled_edges(self):
        compare.beveled_edges(self.m_current_image)

    #LINEAR
    def up_filter(self):
        mask = np.array([[-1, -1, -1],
                 [-1,  9, -1],
                 [-1, -1, -1]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img)
        

    def down_filter(self):
        mask = np.array([[1, 1, 1],
                 [1,  1, 1],
                 [1, 1, 1]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img)

    def horizontal_edge_filter(self):
        mask = np.array([[0, 0, 0],
                 [-1,  1, 0],
                 [0, 0, 0]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img)

    def vertical_edge_filter(self):
        mask = np.array([[0, -1, 0],
                 [0,  1, 0],
                 [0, 0, 0]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img)

    def beveled_edge_filter1(self):
        mask = np.array([[-1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img) 

    def beveled_edge_filter2(self):
        mask = np.array([[0, 0, -1],
                 [0, 1, 0],
                 [0, 0, 0]])
        new_img = linear_f.linear_filter(self.m_current_image, mask)
        display.display_image(new_img) 
   
    #NON-LINEAR
    def median_filter(self):
        new_img = nonlinear_f.median_filter(self.m_current_image)
        display.display_image(new_img) 

    def max_filter(self):
        new_img = nonlinear_f.max_filter(self.m_current_image)
        display.display_image(new_img) 

    def min_filter(self):
        new_img = nonlinear_f.min_filter(self.m_current_image)
        display.display_image(new_img) 

    #START
    def start(self):
        self.m_root.mainloop()


