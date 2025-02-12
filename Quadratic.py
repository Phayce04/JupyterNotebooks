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
from PIL import Image, ImageTk

OUTPUT_PATH = Path().resolve()
ASSETS_PATH = OUTPUT_PATH /"frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
# Function to plot the parabola
current_plot = None  # Initially no plot exists

def plot_parabola(a, b, c, points, vertex):
    global current_plot

    # Remove any existing plot from the canvas
    canvas.delete("default_image")

    if current_plot is not None:
        current_plot.get_tk_widget().destroy()
        current_plot = None

    # Create a new figure
    fig, ax = plt.subplots(figsize=(4, 2.7))
    fig.patch.set_visible(False)
    ax.set_facecolor('white')

    # Use the vertex x-coordinate and extend 5 points to the left and right
    vertex_x = vertex[0]
    x_values = [vertex_x + x for x in range(-5, 6)]  # 5 points left and right of vertex
    y_values = [a * x**2 + b * x + c for x in x_values]

    # Plot the parabola
    # Adjust 'a' to omit '1' if it's 1
    a_str_plot = f"{Fraction(a).limit_denominator()}" if a != 1 else ""
    
    # Adjust 'b' and 'c' to reflect their signs
    b_str_plot = f"+ {Fraction(b).limit_denominator()}" if b > 0 else f"- {abs(Fraction(b).limit_denominator())}"
    c_str_plot = f"+ {Fraction(c).limit_denominator()}" if c > 0 else f"- {abs(Fraction(c).limit_denominator())}"
    
    # Create the label string
    plot_label = f"y = {a_str_plot}x^2 {b_str_plot}x {c_str_plot}"
    
    # Update the plot
    ax.plot(x_values, y_values, label=plot_label, color='blue', lw=2)

    # Plot the 10 points
    x_points, y_points = zip(*points)
    ax.scatter(x_points, y_points, color='red', label='Table Points', zorder=5)

    # Highlight the vertex
    ax.scatter([vertex[0]], [vertex[1]], color='green', s=50, label='Vertex', zorder=5)

    # Add grid, axes, labels, and title
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel('x', fontsize=8)
    ax.set_ylabel('y', fontsize=8)
    ax.set_title('Parabola Plot', fontsize=10)
    ax.legend(fontsize=8)

    # Adjust axis limits
    ax.set_xlim(vertex_x - 5, vertex_x + 5)
    ax.set_ylim(min(y_values) - 5, max(y_values) + 5)
    ax.set_aspect('auto')
    plt.tight_layout()

    # Display the plot on the Tkinter window
    current_plot = FigureCanvasTkAgg(fig, window)
    current_plot.get_tk_widget().place(x=30.0, y=140.0)
    current_plot.draw()


def calculate_and_plot_quadratic():
    try:
        equation_input = entry_1.get()  # Input for the quadratic equation

        if not equation_input:
            raise ValueError("Please provide a quadratic equation.")

        # Remove spaces for easier parsing
        equation_input = equation_input.replace(" ", "").replace("–", "-")

        # Variables to store coefficients and vertex
        a, b, c = None, None, None
        h, k = None, None

        # Parse the equation: Standard form (y = ax^2 + bx + c) or Vertex form (y = a(x-h)^2 + k)
        if "(x" in equation_input and "^2" in equation_input:
            # Vertex form: y = a(x-h)^2 + k
            match = re.match(r"y=([+-]?\d*\.?\d*)\(x([+-]\d*\.?\d*)\)\^2([+-]\d*\.?\d*)", equation_input)
            if match:
                a = float(match.group(1)) if match.group(1) not in ["", "+", "-"] else 1 if match.group(1) in ["", "+"] else -1
                h = -float(match.group(2))
                k = float(match.group(3))
                b = -2 * a * h
                c = a * h**2 + k
            else:
                raise ValueError("Invalid vertex form. Use y = a(x-h)^2 + k")
        elif "x^2" in equation_input:
            # Standard form: y = ax^2 + bx + c
            match = re.match(r"y=([+-]?\d*\.?\d*)x\^2([+-]\d*\.?\d*)x([+-]\d*\.?\d*)", equation_input)
            if match:
                a = float(match.group(1)) if match.group(1) not in ["", "+", "-"] else 1 if match.group(1) in ["", "+"] else -1
                b = float(match.group(2))
                c = float(match.group(3))
                h = -b / (2 * a)
                k = a * h**2 + b * h + c
            else:
                raise ValueError("Invalid standard form. Use y = ax^2 + bx + c")
        else:
            raise ValueError("Unsupported equation format. Use y = ax^2 + bx + c or y = a(x-h)^2 + k.")

        # Calculate the vertex
        vertex = (h, k)

        # Convert to both forms
        h_str = f"x - {Fraction(h).limit_denominator()}" if h >= 0 else f"x + {abs(Fraction(h).limit_denominator())}"
        k_str = f"+ {Fraction(k).limit_denominator()}" if k >= 0 else f"- {abs(Fraction(k).limit_denominator())}"
        # Skip '1' for a if it's 1
        a_str_vertex = f"{Fraction(a).limit_denominator()}" if a != 1 else ""
        vertex_form = f"y = {a_str_vertex}({h_str})^2 {k_str}"
        
        # Convert to standard form
        # Skip '1' for a if it's 1
        a_str_standard = f"{Fraction(a).limit_denominator()}" if a != 1 else ""
        # Adjust b and c for their signs
        b_str = f"+ {Fraction(b).limit_denominator()}" if b > 0 else f"- {abs(Fraction(b).limit_denominator())}"
        c_str = f"+ {Fraction(c).limit_denominator()}" if c > 0 else f"- {abs(Fraction(c).limit_denominator())}"
        standard_form = f"y = {a_str_standard}x^2 {b_str}x {c_str}"

        # Table of values: 5 points left and right of the vertex
        table_values = []
        for x in range(int(h) - 5, int(h) + 6):
            y = a * x**2 + b * x + c
            table_values.append((x, y))

        # Prepare the result text
        result_text = f"Standard Form: {standard_form}\n"
        result_text += f"Vertex Form: {vertex_form}\n"
        result_text += f"Vertex: ({h:.2f}, {k:.2f})\n"
        result_text += "\nTable of Values:\n"
        for x, y in table_values:
            result_text += f"x = {x}, y = {y:.2f}\n"

        # Update the canvas with the result
        canvas.itemconfig(result_label, text=result_text)

        # Plot the parabola
        plot_parabola(a, b, c, table_values, vertex)

    except ValueError as e:
        canvas.itemconfig(result_label, text=f"Error: {e}")

def reset():
    # Clear all input textboxes
    entry_1.delete(0, END)


    # Undelete the default image 
    canvas.delete("plot")  

    # Clear the solutions and table
    canvas.itemconfig(result_label, text="")  

    global current_plot  # Reference the global variable

    if current_plot is not None:
        current_plot.get_tk_widget().destroy()
        current_plot = None  
    canvas.create_text(
    35.0,
    110.0,
    anchor="nw",
    text="Graph",
    fill="#000000",
    font=("Murecho SemiBold", 20 * -1),
    tags="default_image"
    )
    image_path_1 = relative_to_assets("image_1.png")
    image_1 = Image.open(image_path_1)
    width_1, height_1 = image_1.size
    new_width_1 = int(width_1 * 1.3)
    new_height_1 = int(height_1 * 1)
    image_1_resized = image_1.resize((new_width_1, new_height_1))
    image_image_1_resized = ImageTk.PhotoImage(image_1_resized)
    window.image_image_1_resized = image_image_1_resized
    image_1 = canvas.create_image(
        225.0,
        283.0,
        image=image_image_1_resized,
        tags="default_image"
    )

    print("Reset completed.")  

window = Tk()

window.geometry("700x550")
window.configure(bg = "#FFE873")
window.title("Quadratic Equations")


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
    12.0,
    anchor="nw",
    text="Graphing Tool for \nQuadratic Equations",
    fill="#FFFFFF",
    font=("Murecho SemiBold", 32 * -1)
)

canvas.create_rectangle(
    0.0,
    523.0,
    700.0,
    550.0,
    fill="#306998",
    outline="")


canvas.create_text(
    459.0,
    110.0,
    anchor="nw",
    text="Table",
    fill="#000000",
    font=("Murecho SemiBold", 20 * -1)
)

image_path_1 = relative_to_assets("image_1.png")
image_1 = Image.open(image_path_1)
width_1, height_1 = image_1.size
new_width_1 = int(width_1 * 1.3)
new_height_1 = int(height_1 * 1)
image_1_resized = image_1.resize((new_width_1, new_height_1))
image_image_1_resized = ImageTk.PhotoImage(image_1_resized)
window.image_image_1_resized = image_image_1_resized
image_1 = canvas.create_image(
    225.0,
    283.0,
    image=image_image_1_resized,
    tags="default_image"
)

image_path = relative_to_assets("image_2.png")
image = Image.open(image_path)

width, height = image.size
new_width = int(width * 0.7)
new_height = int(height * 1)
image_resized = image.resize((new_width, new_height))
image_image_2_resized = ImageTk.PhotoImage(image_resized)
window.image_image_2 = image_image_2_resized
image_2 = canvas.create_image(
    560.0,
    283.0,
    image=image_image_2_resized
)
canvas.create_text(
    35.0,
    110.0,
    anchor="nw",
    text="Graph",
    fill="#000000",
    font=("Murecho SemiBold", 20 * -1)
)


canvas.create_text(
    59.0,
    431.0,
    anchor="nw",
    text="Enter Equation",
    fill="#306998",
    font=("Murecho SemiBold", 16 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    659.9999967736619,
    43.0,
    image=image_image_3
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    107.0,
    480.0,
    image=entry_image_1
)
entry_1 = Entry(
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




button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=calculate_and_plot_quadratic,  # Call the plot function when the button is clicked
    relief="flat"
)
button_1.place(
    x=359.0,
    y=460.0,
    width=83.0,
    height=40.0
)
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=reset,  # Call the reset function when the button is clicked
    relief="flat"
)
button_2.place(
    x=459.0,
    y=460.0,
    width=83.0,
    height=40.0
)

result_label = canvas.create_text(540, 280, text="", fill="black", font=("Arial", 7))

window.resizable(False, False)
window.mainloop()


# In[ ]:





# In[ ]:




