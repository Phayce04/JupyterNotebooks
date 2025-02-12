#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, END
from tkinter.ttk import Combobox  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import lcm
from fractions import Fraction
from math import gcd
import re 
from tkinter import Toplevel
from linearfunctions import calculate_and_plot, reset, plot_line  # Import functions
from quadraticfunction import calculate_and_plot_quadratic, resetquadratic # Import functions
from PIL import Image, ImageTk

OUTPUT_PATH = Path().resolve()
ASSETS_PATH = OUTPUT_PATH /"frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_linear_window():
    linear_window = Toplevel(window)
    linear_window.geometry("700x550")
    linear_window.configure(bg="#FFE873")
    linear_window.title("Linear Equations")

    # Create a canvas for the new window
    linear_canvas = Canvas(
        linear_window,
        bg="#FFE873",
        height=550,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    linear_canvas.place(x=0, y=0)

    # Add the same UI elements as in the main window
    linear_canvas.create_rectangle(
        0.0,
        0.0,
        700.0,
        94.0,
        fill="#306998",
        outline=""
    )

    linear_canvas.create_text(
        17.0,
        12.0,
        anchor="nw",
        text="Graphing Tool for \nBasic Linear Equations",
        fill="#FFFFFF",
        font=("Murecho SemiBold", 32 * -1)
    )

    linear_canvas.create_rectangle(
        0.0,
        523.0,
        700.0,
        550.0,
        fill="#306998",
        outline=""
    )

    linear_canvas.create_text(
        349.0,
        110.0,
        anchor="nw",
        text="Table",
        fill="#000000",
        font=("Murecho SemiBold", 20 * -1)
    )

    # Add the graph placeholder image
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    linear_window.image_image_1 = image_image_1  
    linear_canvas.create_image(
        175.0,
        283.0,
        image=image_image_1,
        tags="default_image"
    )

    # Add the table placeholder image
    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    linear_window.image_image_2 = image_image_2  
    linear_canvas.create_image(
        520.0,
        283.0,
        image=image_image_2
    )

    linear_canvas.create_text(
        35.0,
        110.0,
        anchor="nw",
        text="Graph",
        fill="#000000",
        font=("Murecho SemiBold", 20 * -1),
        tags="default_image"
    )

    # Add labels for input fields
    linear_canvas.create_text(
        152.0,
        431.0,
        anchor="nw",
        text="Enter Point 1",
        fill="#306998",
        font=("Murecho SemiBold", 16 * -1)
    )

    linear_canvas.create_text(
        284.0,
        431.0,
        anchor="nw",
        text="Enter Point 2",
        fill="#306998",
        font=("Murecho SemiBold", 16 * -1)
    )

    linear_canvas.create_text(
        35.0,
        431.0,
        anchor="nw",
        text="Enter Slope",
        fill="#306998",
        font=("Murecho SemiBold", 16 * -1)
    )

    linear_canvas.create_text(
        416.0,
        431.0,
        anchor="nw",
        text="Enter Equation",
        fill="#306998",
        font=("Murecho SemiBold", 16 * -1)
    )

    # Add entry fields
    entry_1 = Entry(
        linear_window,
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=59.0,
        y=465.0,
        width=96.0,
        height=28.0
    )

    entry_2 = Entry(
        linear_window,
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=196.0,
        y=465.0,
        width=96.0,
        height=28.0
    )

    entry_3 = Entry(
        linear_window,
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=326.0,
        y=465.0,
        width=96.0,
        height=28.0
    )

    entry_4 = Entry(
        linear_window,
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=452.0,
        y=465.0,
        width=96.0,
        height=28.0
    )

    button_1 = Button(
        linear_window,
        text="Plot",
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        command=lambda: calculate_and_plot(entry_1, entry_2, entry_3, entry_4, linear_canvas,result_label)
    )
    button_1.place(
        x=589.0,
        y=475.0,
        width=83.0,
        height=40.0
    )

    button_2 = Button(
        linear_window,
        text="Reset",
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        command=lambda: reset(entry_1, entry_2, entry_3, entry_4, linear_canvas,result_label)
    )
    button_2.place(
        x=589.0,
        y=425.0,
        width=83.0,
        height=40.0
    )

    # Add a result label
    result_label = linear_canvas.create_text(
        500, 280,
        text="",
        fill="black",
        font=("Arial", 7)
    )
def open_quadratic_window():
    quadratic_window = Toplevel(window)
    quadratic_window.geometry("700x550")
    quadratic_window.configure(bg="#FFE873")
    quadratic_window.title("Quadratic Equations")

    # Create a canvas for the new window
    quadratic_canvas = Canvas(
        quadratic_window,
        bg="#FFE873",
        height=550,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    quadratic_canvas.place(x=0, y=0)

    # Add the same UI elements as in the main window
    quadratic_canvas.create_rectangle(
        0.0,
        0.0,
        700.0,
        94.0,
        fill="#306998",
        outline=""
    )

    quadratic_canvas.create_text(
        17.0,
        12.0,
        anchor="nw",
        text="Graphing Tool for \nQuadratic Equations",
        fill="#FFFFFF",
        font=("Murecho SemiBold", 32 * -1)
    )

    quadratic_canvas.create_rectangle(
        0.0,
        523.0,
        700.0,
        550.0,
        fill="#306998",
        outline=""
    )

    quadratic_canvas.create_text(
        459.0,
        110.0,
        anchor="nw",
        text="Table",
        fill="#000000",
        font=("Murecho SemiBold", 20 * -1)
    )

    # Add the graph placeholder image
    image_path_1 = relative_to_assets("image_1.png")
    image_1 = Image.open(image_path_1)
    width_1, height_1 = image_1.size
    new_width_1 = int(width_1 * 1.3)
    new_height_1 = int(height_1 * 1)
    image_1_resized = image_1.resize((new_width_1, new_height_1))
    image_image_1_resized = ImageTk.PhotoImage(image_1_resized)
    window.image_image_1_resized = image_image_1_resized
    image_1 = quadratic_canvas.create_image(
        225.0,
        283.0,
        image=image_image_1_resized,
        tags="default_image"
    )

    # Add the table placeholder image
    image_path = relative_to_assets("image_2.png")
    image = Image.open(image_path)

    width, height = image.size
    new_width = int(width * 0.7)
    new_height = int(height * 1)
    image_resized = image.resize((new_width, new_height))
    image_image_2_resized = ImageTk.PhotoImage(image_resized)
    window.image_image_2 = image_image_2_resized
    image_2 = quadratic_canvas.create_image(
        560.0,
        283.0,
        image=image_image_2_resized
    )

    quadratic_canvas.create_text(
        35.0,
        110.0,
        anchor="nw",
        text="Graph",
        fill="#000000",
        font=("Murecho SemiBold", 20 * -1),
        tags="default_image"
    )

    # Add labels for input fields
    quadratic_canvas.create_text(
        59.0,
        431.0,
        anchor="nw",
        text="Enter Equation",
        fill="#306998",
        font=("Murecho SemiBold", 16 * -1)
    )

    # Add entry fields
    entry_1 = Entry(
        quadratic_window,
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=49.0,
        y=465.0,
        width=296.0,
        height=35.0
    )

    button_1 = Button(
        quadratic_window,
        text="Plot",
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        command=lambda: calculate_and_plot_quadratic(entry_1, quadratic_canvas, result_label)
    )
    button_1.place(
        x=359.0,
        y=460.0,
        width=83.0,
        height=40.0
    )

    button_2 = Button(
        quadratic_window,
        text="Reset",
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        command=lambda: resetquadratic(entry_1, quadratic_canvas, result_label)
    )
    button_2.place(
        x=459.0,
        y=460.0,
        width=83.0,
        height=40.0
    )

    # Add a result label
    result_label = quadratic_canvas.create_text(
        540, 280,
        text="",
        fill="black",
        font=("Arial", 7)
    )
window = Tk()

window.geometry("700x550")
window.configure(bg = "#FFE873")
window.title("Topic 2-4: Linear Equations")


canvas = Canvas(
    window,
    bg = "#FFE873",
    height = 550,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    700.0,
    94.0,
    fill="#306998",
    outline="")

canvas.create_text(
    17.0,
    18.0,
    anchor="nw",
    text="Pontiga Midterm Project",
    fill="#FFFFFF",
    font=("Murecho SemiBold", 50 * -1)
)

canvas.create_rectangle(
    0.0,
    523.0,
    700.0,
    550.0,
    fill="#306998",
    outline="")


button_1 = Button(
    text="Linear",
    font=("Arial", 20, "bold"),
    bg="#2196F3",
    fg="white",
    borderwidth=3,
    relief="raised",
    command=open_linear_window  # This makes it open the new window
)
button_1.place(
    x=225.0,
    y=150.0,
    width=250.0,
    height=70.0
)
button_2 = Button(
    text="Quadratic",
    font=("Arial", 20, "bold"),  # Increased font size
    bg="#2196F3",  # Blue background
    fg="white",
    borderwidth=3,
    relief="raised",
    command=open_quadratic_window
)
button_2.place(
    x=225.0,  # Adjusted for centering
    y=240.0,  # Adjusted position
    width=250.0,  # Increased width
    height=70.0  # Increased height
)

button_3 = Button(
    text="Exponential",
    font=("Arial", 20, "bold"),  # Increased font size
    bg="#2196F3",  # Blue background
    fg="white",
    borderwidth=3,
    relief="raised"
)
button_3.place(
    x=225.0,  # Adjusted for centering
    y=330.0,  # Adjusted position
    width=250.0,  # Increased width
    height=70.0  # Increased height
)



window.resizable(False, False)
window.mainloop()


# In[ ]:





# In[ ]:




