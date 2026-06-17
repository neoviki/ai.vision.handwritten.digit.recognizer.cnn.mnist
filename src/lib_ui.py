'''
    Simple User Interface to create image Recognition Application

Author:

Vignesh (a) Viki
www.viki.design
'''

'''
Dependencies

sudo apt-get install python3-pil.imagetk
sudo pip3 install Pillow
'''

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from lib_logger import *
import sys


log = logger()


color_bg = "#ffffff"          # main window / frame background
color_fg = "#000000"          # normal text color

color_canvas_bg = "#ffffff"   # canvas background

color_button_bg = "#f2f2f2"   # button background
color_button_fg = "#000000"   # button text

color_border = "#808080"      # gray border
color_active_bg = "#e0e0e0"   # button active background
color_active_fg = "#000000"   # button active text


try:
    resample = Image.Resampling.LANCZOS  # Pillow >= 10.0
except AttributeError:
    resample = Image.ANTIALIAS           # Pillow < 10.0


font_list = [
    'texgyretermes',
    'fangsong ti',
    'fixed',
    'clearlyu alternate glyphs',
    'latin modern roman',
    'open look glyph',
    'texgyrechorus',
    'latin modern  typewriter',
    'song ti',
    'open look cursor',
    'newspaper',
    'texgyrecursor',
    'clearlyu ligature',
    'mincho',
    'clearlyu devangari extra',
    'clearlyu pua',
    'texgyreheros',
    'texgyrebonum',
    'clearlyu',
    'texgyreschola',
    'latin modern typewriter variable width',
    'latin modern sans',
    'texgyreadventor',
    'clean',
    'nil',
    'clearlyu arabic',
    'clearlyu devanagari',
    'texgyrepagella',
    'latin modern sansquotation',
    'gothic',
    'clearlyu arabic extra'
]


ctr = 0

__Input_Image_Name__ = ""
__ColorCode__ = 0

__canvas1__ = None
__canvas2__ = None

open_path = "."


# expects a function external_callback(file_name)

def set_input_image(name):
    global __Input_Image_Name__
    __Input_Image_Name__ = name


def get_input_image():
    return __Input_Image_Name__


def classify_image_callback(gui, canvas, external_callback):
    global __canvas1__, __canvas2__
    global __ColorCode__

    canvas.delete("all")

    classified_output = "None"

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    fname = get_input_image()

    if __ColorCode__ == 0:
        color = "gray40"
        __ColorCode__ = 1
    else:
        color = "gray70"
        __ColorCode__ = 0

    if not external_callback or not fname:
        print("info(): no external callback")
        classified_output = "NO CALLBACK / NO INPUT"
        font_size = 30
    else:
        classified_output = external_callback(fname)
        font_size = 120

    s = str(classified_output)

    canvas.create_text(
        canvas_width / 2,
        canvas_height / 2,
        font=(font_list[0], font_size),
        text=s,
        fill=color
    )

    return


def browse_image_callback(gui, canvas, fname):
    global __canvas1__, __canvas2__, open_path

    canvas.delete("all")
    __canvas2__.delete("all")

    try:
        fname = filedialog.askopenfilename(initialdir=open_path)
    except:
        print("error(): file browse")
        return

    if not fname:
        print("info(): file name is empty")
        set_input_image(None)
        return

    print("file_name = " + fname)
    set_input_image(fname)

    try:
        image = Image.open(fname)
    except:
        print("error(): fopen")
        return

    image_width = float(image.size[0])
    image_height = float(image.size[1])

    new_width = 200

    percent_change_in_width = float(new_width / image_width)
    new_height = int(image_height * percent_change_in_width)

    image = image.resize((new_width, new_height), resample)

    photo = ImageTk.PhotoImage(image)

    canvas.delete("all")
    canvas.image = photo

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    canvas.create_image(
        canvas_width / 2,
        canvas_height / 2,
        image=photo
    )

    return


def browse_image_frame(gui, canvas, fname):
    frame1 = tk.Frame(
        gui,
        width=500,
        height=500,
        bd=2,
        background=color_bg,
        highlightbackground=color_border,
        highlightcolor=color_border,
        highlightthickness=1
    )

    frame1.grid(row=1, column=0)

    canvas = tk.Canvas(
        frame1,
        height=390,
        width=490,
        background=color_canvas_bg,
        bd=4,
        relief=tk.RAISED,
        highlightbackground=color_border,
        highlightcolor=color_border,
        highlightthickness=1
    )

    canvas.grid(row=1, column=0)

    b_image = tk.Button(
        master=frame1,
        text='Browse Image',
        height=2,
        width=15,
        command=lambda: browse_image_callback(gui, canvas, fname),
        background=color_button_bg,
        foreground=color_button_fg,
        activebackground=color_active_bg,
        activeforeground=color_active_fg,
        highlightbackground=color_border,
        highlightcolor=color_border,
        bd=2,
        relief=tk.RAISED
    )

    b_image.grid(row=0, column=0, padx=4, pady=4)

    return canvas


def classify_image_frame(gui, canvas, external_callback):
    frame2 = tk.Frame(
        gui,
        width=500,
        height=500,
        bd=2,
        background=color_bg,
        highlightbackground=color_border,
        highlightcolor=color_border,
        highlightthickness=1
    )

    frame2.grid(row=1, column=1)

    canvas = tk.Canvas(
        frame2,
        height=390,
        width=490,
        background=color_canvas_bg,
        bd=4,
        relief=tk.SUNKEN,
        highlightbackground=color_border,
        highlightcolor=color_border,
        highlightthickness=1
    )

    canvas.grid(row=1, column=1)

    b_classify = tk.Button(
        master=frame2,
        text='Classify Image',
        height=2,
        width=15,
        command=lambda: classify_image_callback(gui, canvas, external_callback),
        background=color_button_bg,
        foreground=color_button_fg,
        activebackground=color_active_bg,
        activeforeground=color_active_fg,
        highlightbackground=color_border,
        highlightcolor=color_border,
        bd=2,
        relief=tk.RAISED
    )

    b_classify.grid(row=0, column=1, padx=4, pady=4)

    return canvas


def render(external_callback, default_images_path):
    global __canvas1__, __canvas2__, open_path

    fname = ""
    open_path = default_images_path

    canvas_1 = None
    canvas_2 = None

    gui = tk.Tk()

    gui.configure(bg=color_bg)
    gui.wm_title("CONVOLUTIONAL NEURAL NETWORK IMAGE CLASSIFIER")

    # Handle close button
    def on_close():
        print(log._if + "Closing UI")
        gui.destroy()
        sys.exit(0)

    gui.protocol("WM_DELETE_WINDOW", on_close)

    # Bind 'q' key to quit
    def on_key_press(event):
        if event.char == 'q':
            print(log._if + "Key press detected ('q') : Closing GUI.")
            gui.destroy()
            sys.exit(0)

    gui.bind("<Key>", on_key_press)

    canvas_1 = browse_image_frame(gui, canvas_1, fname)
    canvas_2 = classify_image_frame(gui, canvas_2, external_callback)

    __canvas1__ = canvas_1
    __canvas2__ = canvas_2

    tk.mainloop()
