'''
Simple User Interface to create image Recognization Application

Author:

V Natarajan (a) Viki
www.viki.design

'''

'''

Dependencies

sudo apt-get install python3-pil.imagetk
sudo apt-get install python3-pil.imagetk
sudo pip3 install Pillow


'''
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import ImageTk, Image

font_list=['texgyretermes', 'fangsong ti', 'fixed', 'clearlyu alternate glyphs', 'latin modern roman', 'open look glyph', 'texgyrechorus', 'latin modern  typewriter', 'song ti', 'open look cursor', 'newspaper', 'texgyrecursor', 'clearlyu ligature', 'mincho', 'clearlyu devangari extra', 'clearlyu pua',      'texgyreheros', 'texgyrebonum', 'clearlyu', 'texgyreschola', 'latin modern typewriter variable width', 'latin modern sans', 'texgyreadventor', 'clean',   'nil', 'clearlyu arabic', 'clearlyu devanagari', 'texgyrepagella', 'latin modern sansquotation', 'gothic', 'clearlyu arabic extra']


#Compatibility handling
try:
    resample = Image.Resampling.LANCZOS
except AttributeError:
    resample = Image.ANTIALIAS  # For Pillow <10

ctr = 0

open_path = "../sample_images"

__Input_Image_Name__ = ""
__ColorCode__ = 0

__canvas1__ = None
__canvas2__ = None

#expects a function external_callback(file_name)

def set_input_image(name):
    global __Input_Image_Name__
    __Input_Image_Name__ = name

def get_input_image():
    return __Input_Image_Name__

def browse_image_callback(gui, canvas, fname):
    fname = None
    global __canvas1__, __canvas2__

    canvas.delete("all")
    __canvas2__.delete("all")

    try:
        fname =  filedialog.askopenfilename(initialdir = open_path)
    except:
        print ("error(): file browse")
        return

    if not fname:
        print ("info(): file name is empty")
        set_input_image(None)
        return

    print ("file_name = "+fname)
    set_input_image(fname)

    try:
        image = Image.open(fname)
    except:
        print ("error(): fopen")
        return
    image_width =   float(image.size[0])
    image_height =  float(image.size[1])
    new_width = 200
    percent_change_in_width = float(float(new_width) / float(image_width))
    new_height = int(image_height * percent_change_in_width)
    image = image.resize((new_width, new_height), resample)
    photo = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.image = photo

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    canvas.create_image(  canvas_width/2, canvas_height/2,
                            image=photo
                        )
    return

def classify_image_callback(gui, canvas, external_callback):
    global __canvas1__, __canvas2__
    global __ColorCode__
    canvas.delete("all")
    classified_output = "None"
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    fname = get_input_image()

    if __ColorCode__ == 0:
        color = "gray44"
        __ColorCode__=1
    else:
        color = "gray90"
        __ColorCode__=0

    if not external_callback or not fname:
        print("info(): no external callback");
        classified_output = "NO CALLBACK / NO INPUT"
        font_size = 30
    else:
        classified_output = external_callback(fname)
        font_size = 120

    s = str(classified_output)
    canvas.create_text(   canvas_width/2, canvas_height/2, font=(font_list[0], font_size),
                            text=s, fill=color
                            )

    return

def browse_image_frame(gui, canvas, fname):
    frame1 = tk.Frame(gui, width=500, height=500, bd=2, background='#2d2d2d')
    frame1.grid(row=1, column=0)
    canvas = tk.Canvas(frame1, height=390, width=490,
                       background="#1e1e1e", bd=4, relief=tk.RAISED,
                       highlightthickness=0)
    canvas.grid(row=1,column=0)
    b_image = tk.Button(master=frame1,
                        text='Browse Image',
                        height=2, width=15,
                        command=lambda: browse_image_callback(gui, canvas, fname),
                        background='#3c3c3c',
                        foreground='#dcdcdc',
                        activebackground='#505050',
                        activeforeground='#ffffff',
                        highlightbackground='#444444',
                        highlightcolor='#aaaaaa'
                        )
    b_image.grid(row=0, column=0, padx=4, pady=4)
    return canvas

def classify_image_frame(gui, canvas, external_callback):
    frame2 = tk.Frame(gui, width=500, height=500, bd=2, background='#2d2d2d')
    frame2.grid(row=1, column=1)
    canvas = tk.Canvas(frame2, height=390, width=490,
                       background="#1e1e1e", bd=4, relief=tk.SUNKEN,
                       highlightthickness=0)
    canvas.grid(row=1,column=1)
    b_classify = tk.Button(master=frame2,
                           text='Classify Image',
                           height=2,
                           width=15,
                           command=lambda: classify_image_callback(gui, canvas, external_callback),
                           background='#3c3c3c',
                           foreground='#dcdcdc',
                           activebackground='#505050',
                           activeforeground='#ffffff',
                           highlightbackground='#444444',
                           highlightcolor='#aaaaaa'
                           )
    b_classify.grid(row=0, column=1, padx=4, pady=4)
    return canvas

def render(external_callback):
    global __canvas1__, __canvas2__
    fname = ""
    canvas_1 = None
    canvas_2 = None
    gui = tk.Tk()
    gui.configure(bg='#1e1e1e')  # main window background
    gui.wm_title("CONVOLUTIONAL NEURAL NETWORK HANDWRITTEN DIGIT CLASSIFIER")
    canvas_1 = browse_image_frame(gui, canvas_1, fname)
    canvas_2 = classify_image_frame(gui, canvas_2, external_callback)
    __canvas1__ = canvas_1
    __canvas2__ = canvas_2
    tk.mainloop()

#render(None)
