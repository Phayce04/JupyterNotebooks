from tkinter import END
import re
import numpy as np

from fractions import Fraction
from math import gcd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_exponential(a, b, c, h, k, points, canvas):
    global current_plot

    # Remove any existing plot from the canvas
    canvas.delete("plot")

    # Create a new figure
    fig, ax = plt.subplots(figsize=(4, 2.7))
    fig.patch.set_visible(False)
    ax.set_facecolor('white')

    # Generate x values (5 units left and right of the asymptote x = h)
    x_values = np.linspace(h - 5, h + 5, 100)
    y_values = a * (b ** (c * (x_values - h))) + k  # Exponential function

    # Generate integer x points (matching the equation)
    x_int_values = range(int(h - 5), int(h + 6))
    y_int_values = [a * (b ** (c * (x - h))) + k for x in x_int_values]

    # Format equation for display
    formatted_c = f"{c}x" if c != 1 else "x"
    formatted_h = f"- {abs(h)}" if h > 0 else f"+ {abs(h)}"
    formatted_k = f"+ {k}" if k > 0 else f"- {abs(k)}"

    plot_label = f"y = {a} * {b}^({formatted_c} {formatted_h}) {formatted_k if k != 0 else ''}".strip()

    # Plot the exponential curve
    ax.plot(x_values, y_values, label=plot_label, color='blue', lw=2)

    # Plot integer points
    for x, y in points:
        ax.scatter(x, y, color='red', zorder=5)
        ax.text(x, y, f'({x},{y:.2f})', fontsize=7, verticalalignment='bottom', horizontalalignment='right')

    # Draw the horizontal asymptote (dashed green line at y = k)
    ax.axhline(y=k, color='green', linestyle='dashed', linewidth=1, label=f"Asymptote: y = {k}")

    # Add grid, axes, labels, and title
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel('x', fontsize=8)
    ax.set_ylabel('y', fontsize=8)
    ax.set_title('Exponential Plot', fontsize=10)
    ax.legend(fontsize=8)

    # Adjust axis limits dynamically
    y_min = min(y_values) - abs(k * 0.1)  # Expand lower bound slightly
    y_max = max(y_values) + abs(k * 0.1)  # Expand upper bound slightly

    ax.set_xlim(h - 6, h + 6)
    ax.set_ylim(y_min, y_max)

    ax.set_aspect('auto')
    plt.tight_layout()

    # Display the plot in Tkinter canvas
    current_plot = FigureCanvasTkAgg(fig, canvas.master)
    current_plot.get_tk_widget().place(x=30.0, y=145.0)
    current_plot.draw()


def calculate_and_plot_exponential(entry_1, canvas, result_label):
    try:
        equation_input = entry_1.get().replace(" ", "").replace("–", "-")  # Normalize input
        
        if not equation_input:
            raise ValueError("Please provide an exponential equation.")

        # Updated regex: Supports negative b, exponent, and optional multiplication
        pattern = r"y=(-)?(?:([\d]*\.?\d+)?\*)?(-?\d+|e)\^\(?([-]?\d*x|[-]?\d+|x)?([-+]\d+)?\)?([-+]\d+)?"

        match = re.match(pattern, equation_input)
        if not match:
            raise ValueError("Invalid format. Use y = a * b^(cx-h) + k.")

        neg_b, a_str, b_str, c_str, h_str, k_str = match.groups()

        a = float(a_str) if a_str else 1
        b = np.e if b_str == "e" else float(b_str)

        if neg_b:  # If `b` was negative, adjust it
            a *= -1  # Multiply `a` by -1
            b = abs(b)  # Make `b` positive
        if c_str in ["x", None]:  
            c = 1.0  
        elif c_str == "-x":  
            c = -1.0  
        else:  
            c = float(c_str.replace("x", ""))  # Remove "x" and convert to float

        h = float(Fraction(h_str)) if h_str else 0  # Default `h` to 0
        k = float(Fraction(k_str)) if k_str else 0  # Default `k` to 0

        # Generate table of values (-5 to 5)
        table_values = [(x, a * (b ** (c * x - h)) + k) for x in range(int(h - 5), int(h + 6))]

        # **Correctly Format the Equation**
        formatted_c = f"{c}x" if c != 1 else "x"
        formatted_h = f"- {abs(h)}" if h > 0 else f"+ {abs(h)}"
        formatted_k = f"+ {k}" if k > 0 else f"- {abs(k)}"

        equation_str = f"y = {a} * {b}^({formatted_c} {formatted_h}) {formatted_k if k != 0 else ''}".strip()

        # Prepare result text
        asymptote = k  # Horizontal asymptote
        result_text = f"Asymptote: y = {asymptote:.2f}\n\n"
        result_text += "Table of Values:\n"
        result_text += "\n".join([f"x = {x}, y = {y:.2f}" for x, y in table_values])

        # Update the result label
        canvas.itemconfig(result_label, text=result_text)

        # Required function call
        plot_exponential(a, b, c, h, k, table_values, canvas)

    except Exception as e:
        canvas.itemconfig(result_label, text=f"Error: {e}")


def reset_exponential(entry_1, canvas, result_label):
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