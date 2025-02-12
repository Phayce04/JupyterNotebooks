
from tkinter import END
import re
from fractions import Fraction
from math import gcd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_parabola(a, b, c, points, vertex, canvas):
    global current_plot

    # Remove any existing plot from the canvas
    canvas.delete("plot")

    # Create a new figure
    fig, ax = plt.subplots(figsize=(4, 2.7))
    fig.patch.set_visible(False)
    ax.set_facecolor('white')

    # Use the vertex x-coordinate and extend 5 points to the left and right
    vertex_x = vertex[0]
    x_values = [vertex_x + x for x in range(-5, 6)]  # 5 points left and right of vertex
    y_values = [a * x**2 + b * x + c for x in x_values]

    # Plot the parabola
    a_str_plot = f"{int(a)}" if a != 1 else ""
    b_str_plot = f"+ {int(b)}" if b > 0 else f"- {abs(int(b))}"
    c_str_plot = f"+ {int(c)}" if c > 0 else f"- {abs(int(c))}"
    plot_label = f"y = {a_str_plot}x² {b_str_plot}x {c_str_plot}"

    ax.plot(x_values, y_values, label=plot_label, color='blue', lw=2)

    # Plot the 10 points and label them as integers
    for x, y in points:
        ax.scatter(x, int(y), color='red', zorder=5)
        ax.text(x, int(y), f'({x},{int(y)})', fontsize=7, verticalalignment='bottom', horizontalalignment='right')

    # Highlight the vertex without labeling
    ax.scatter([vertex[0]], [vertex[1]], color='green', s=50, zorder=5)

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
    current_plot = FigureCanvasTkAgg(fig, canvas.master)  
    current_plot.get_tk_widget().place(x=30.0, y=145.0)
    current_plot.draw()


def calculate_and_plot_quadratic(entry_1, canvas, result_label):
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
        plot_parabola(a, b, c, table_values, vertex,canvas)

    except ValueError as e:
        canvas.itemconfig(result_label, text=f"Error: {e}")

def resetquadratic(entry_1, canvas, result_label):
    # Clear all input textboxes
    entry_1.delete(0, END)


    # Undelete the default image 
    canvas.delete("plot")  

    # Clear the solutions and table
    canvas.itemconfig(result_label, text="")  


  
    canvas.create_text(
    35.0,
    110.0,
    anchor="nw",
    text="Graph",
    fill="#000000",
    font=("Murecho SemiBold", 20 * -1),
    tags="default_image"
    )


    print("Reset completed.")  