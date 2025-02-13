#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import END
import re
from fractions import Fraction
from math import gcd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_and_plot(entry_1, entry_2, entry_3, entry_4, canvas, result_label):
    try:
        point1 = None
        point2 = None
        slope = None
        intercept = None
        
        # Get input values
        slope_input = entry_1.get() 
        point1_input = entry_2.get()  
        point2_input = entry_3.get() 
        equation_input = entry_4.get() 

        # Initialize variables
        slope = None
        intercept = None

        # Prioritize Equation Input
        if equation_input:
            # Remove spaces
            equation_input = equation_input.replace(" ", "")
            # General Form
            if "x" in equation_input and "y" in equation_input and "=" in equation_input and not equation_input.startswith("y=") and "(x" not in equation_input and not re.match(r"^\d+x=", equation_input):
                left_side, right_side = equation_input.split("=")
                right_side = float(right_side)
                terms = left_side.replace(" ", "").replace("-", "+-").split("+")  # Split into terms, handling both signs
                
                A = B = 0
                for term in terms:
                    if "x" in term:
                        A = float(term.replace("x", "").strip() if term != "x" else "1") 
                    elif "y" in term:
                        B = float(term.replace("y", "").strip() if term != "y" else "1")  
                
                slope = -A / B if B != 0 else 0  
                intercept = right_side / B if B != 0 else 0  
             # Point-Slope Form
            elif "y" in equation_input and "=" in equation_input and "(x" in equation_input: 
                match = re.match(r"y\s*([\+\-]?\s*\d*\.?\d*)\s*=\s*([\+\-]?\d*\.?\d+(?:/\d*\.?\d+)?)\s*\(x\s*([\+\-]?\s*\d*\.?\d*)\)", equation_input)
                
                if match:
                    y_part = match.group(1).strip()
                    slope_part = match.group(2).strip()
                    x_part = match.group(3).strip()
            
                    y1 = float(y_part.replace(' ', '').replace('+', '') if y_part else 0)  
                    slope = float(slope_part)
                    x1 = float(x_part.replace('(', '').replace(')', '').replace(' ', '').replace('+', '') if x_part else 0)  
                    intercept = -(y1 - slope * x1 ) 
                else:
                    raise ValueError("Invalid point-slope format. Example: y + 2 = 3(x - 1)")

             # Slope-Intercept Form
            elif "y=" in equation_input and "(x" not in equation_input:  
                left_side, right_side = equation_input.split("=")
                if "x" in right_side:
                    parts = right_side.split("x")
                    slope = float(parts[0].strip() if parts[0].strip() not in ["", "+", "-"] else "1" if parts[0] == "" else "-1")  
                    intercept = float(parts[1].strip()) if len(parts) > 1 else 0
                else:
                    slope = 0
                    intercept = float(right_side)

            # If there is a transform equation problem or horizontal line
            elif re.match(r"^(\d*x=|x=)", equation_input): 
                if "y" in equation_input:
                    left_side, right_side = equation_input.split("=")
                    left_side = left_side.strip()  
                    right_side = right_side.strip()  
                    
                    x_coefficient = float(left_side.replace("x", "").strip() if left_side != "x" else "1")
                    
                    if "y" in right_side:
                        parts = right_side.split("y")
                        y_coefficient = float(parts[0].strip() if parts[0].strip() not in ["", "+", "-"] else "1" if parts[0] == "" else "-1")             
                        intercept_value = float(parts[1].strip()) if len(parts) > 1 else 0
                    else:
                        y_coefficient = 0
                        intercept_value = float(right_side)
                    
                    if y_coefficient != 0:
                        slope = x_coefficient / y_coefficient  
                    else:
                        slope = 0  
                    if y_coefficient != 0:
                        intercept = intercept_value / -y_coefficient
                    else:
                        intercept = intercept_value  
                else:
                    slope = 0
                    intercept = 0
            else:
                raise ValueError("Unsupported equation format. Use y=mx+b, y-y1=m(x-x1), or Ax+By=C.")
        else:
            # Use other inputs if equation is not provided
            slope = float(slope_input) if slope_input else None
            point1 = None
            if point1_input:
                try:
                    point1 = tuple(map(float, point1_input.split(',')))
                    if len(point1) != 2:
                        raise ValueError("Point must have exactly two coordinates.")
                except Exception:
                    raise ValueError("Invalid Point 1 format. Use the format x,y.")
            
            point2 = None
            if point2_input:
                try:
                    point2 = tuple(map(float, point2_input.split(',')))
                    if len(point2) != 2:
                        raise ValueError("Point must have exactly two coordinates.")
                except Exception:
                    raise ValueError("Invalid Point 2 format. Use the format x,y.")

            if point1 and point2:
                x1, y1 = point1
                x2, y2 = point2
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
                intercept = y1 - slope * x1
            elif slope is not None and point1:
                intercept = point1[1] - slope * point1[0]
            else:
                raise ValueError("Provide either an equation, a slope with a valid point, or two points.")

        # Calculate X-Intercept: Set y = 0 in the equation y = mx + b
        x_intercept = -intercept / slope if slope != 0 else None

        # Prepare all forms of the equation
        slope_fraction = Fraction(slope).limit_denominator()
        intercept_fraction = Fraction(intercept).limit_denominator()
        
        # Slope-intercept form
        if intercept < 0:
            slope_intercept_form = f"Slope-Intercept Form: y = {slope_fraction}x - {abs(intercept_fraction)}"
        else:
            slope_intercept_form = f"Slope-Intercept Form: y = {slope_fraction}x + {intercept_fraction}"

        # Point-Slope Form
        if point1: 
            x1, y1 = point1
            point_slope_form = f"Point-Slope Form: y - {Fraction(y1).limit_denominator()} = {Fraction(slope).limit_denominator()}(x - {Fraction(x1).limit_denominator()})"
        else:  # Default to x - 0
            point_slope_form = f"Point-Slope Form: y - {Fraction(intercept).limit_denominator()} = {Fraction(slope).limit_denominator()}(x - 0)"

        # Standard Form
        A = -slope if slope else 0
        B = 1  
        C = intercept if intercept else 0
        
        A_fraction = Fraction(A).limit_denominator()  
        B_fraction = Fraction(B).limit_denominator()  
        C_fraction = Fraction(C).limit_denominator()  
        
        lcd = A_fraction.denominator * B_fraction.denominator * C_fraction.denominator
        
        A = A_fraction * lcd
        B = B_fraction * lcd
        C = C_fraction * lcd
        
        A = int(A.numerator)
        B = int(B.numerator)
        C = int(C.numerator)

        gcf = gcd(gcd(A, B), C)

        A = A.numerator // gcf
        B = B.numerator // gcf
        C = C.numerator // gcf
        if A < 0:
            A *= -1
            B *= -1
            C *= -1

        if B < 0:
            standard_form = f"Standard Form: {A}x - {abs(B)}y = {C}"
        else:
            standard_form = f"Standard Form: {A}x + {B}y = {C}"

        # Prepare the solution and the table
        result_text = slope_intercept_form + "\n"
        result_text += point_slope_form + "\n"
        result_text += standard_form + "\n\n"
        result_text += f"Slope: {slope}\n"
        result_text += f"Y-Intercept: {intercept}\n"
        if x_intercept is not None:
            result_text += f"X-Intercept: {x_intercept:.2f}\n"
        else:
            result_text += "X-Intercept: Undefined (vertical line)\n"

        # Table of values for x = -5 to 5
        table_values = []
        for x in range(-5, 6):
            y = slope * x + intercept
            table_values.append(f"x = {x}, y = {y:.2f}")
        result_text += "\nTable of Values:\n" + "\n".join(table_values)
        canvas.itemconfig(result_label, text=f"{result_text}")

        # Plot the line by calling the function
        plot_line(slope, intercept, canvas)
    except ValueError as e:
        canvas.itemconfig(result_label, text=f"Error: {e}")


def plot_line(slope, intercept, canvas, min_x=-5, max_x=5):
    # Remove the default placeholders and previous plots if there were any
    canvas.delete("default_image") 
    
    # Create a new figure
    fig, ax = plt.subplots(figsize=(3.2, 2.8))  # Set figure size 
    fig.patch.set_visible(False)
    ax.set_facecolor('white')
    
    # Calculate y-values for the line equation
    x_values = list(range(min_x, max_x + 1))
    y_values = [slope * x + intercept for x in x_values]
    
    # Plot the line
    ax.plot(x_values, y_values, label=f'y = {Fraction(slope).limit_denominator()}x + {intercept}', color='blue', lw=2)
    
    # Plot and label points
    for x, y in zip(x_values, y_values):
        ax.scatter(x, y, color='red', zorder=3)  # Mark points in red
        ax.text(x, y, f'({x},{y})', fontsize=7, verticalalignment='bottom', horizontalalignment='right')
    
    # Add grid, axes, labels, and title
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(color='gray', linestyle='--', linewidth=0.7)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(-8, 8))
    ax.set_xlabel('x', fontsize=8)
    ax.set_ylabel('y', fontsize=8)
    ax.set_title('Cartesian Plane with Line', fontsize=8)
    ax.legend()
    
    # Set axis limits and aspect ratio
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(-10, 10)
    ax.set_aspect('auto')

    # Remove the surrounding box layout
    ax.set_frame_on(False)

    plt.tight_layout()
    
    # Display the plot on the Tkinter window
    current_plot = FigureCanvasTkAgg(fig, canvas.master)  # Track the current plot
    current_plot.get_tk_widget().place(x=30.0, y=130.0)
    current_plot.draw()



def reset(entry_1, entry_2, entry_3, entry_4, canvas,result_label):
    # Clear all input textboxes
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry_4.delete(0, END)

    # Undelete the default image 
    canvas.delete("plot")  

    # Clear the solutions and table
    canvas.itemconfig(result_label, text="")  

    # Reset the plot
    canvas.delete("default_image")
    canvas.create_text(
        35.0,
        110.0,
        anchor="nw",
        text="Graph",
        fill="#000000",
        font=("Murecho SemiBold", 20 * -1),
        tags="default_image"
    )

