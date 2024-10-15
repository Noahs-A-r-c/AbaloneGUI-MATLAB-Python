import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import csv 

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

import datetime
import getpass
import time

import os

from B_Model_Class import BModelClass

# it works only windows.
username = getpass.getuser()

# Set the time to synchronize file reading with the BLE script
now = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M')
print(now)

# Global variables for canvas and axes
canvas = None
ax = None
coordinates = [(0,0,0)]
# Global variables for storing plot values
x_plot_values = []  # Initialize as an empty list
y_plot_values = []  # Initialize as an empty list

# Add a global variable to track the scheduled call
plot_after_id = None

# Set sleep times to affect plotting frequency
sleep_time_ms = 500
sleep_time_s = .5

# Function to add a value to each element in a tuple
def add_to_tuple_elements(tup, value):
    return tuple(element + value for element in tup)


def get_csv_coordinates(username, now):
    global sleep_time_s

    coordinates = []
    logPath = 'C:/Users/' + username + '/Downloads/' + now + '_ABALONE.csv'

    # Wait until the file exists
    while not os.path.exists(logPath):
        time.sleep(sleep_time_s)  # Wait for 1 second before checking again

    with open(logPath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                # for BML Device 1 it is row[1:4]
                xs, ys, zs = map(int, row[2:5])
                # # for BML Device 2 it is row[2:5]
                # xs, ys, zs = map(int, row[2:5])
                coordinates.append((xs,ys,zs))
            except ValueError:
                # handle case where int conversion fails
                    continue
    return coordinates


# simple matplotlib setup function
def setup_plot_range(ax_in):
    ax_in.set_title("Magnetometer Tracking on a 2D Plane from a Magnetic Dipole (110 mT)")
    ax_in.set_xlabel("X-Axis Position (mm)")

    # Set X ticks with more intermediate steps
    ax_in.set_xticks(range(-300, 301, 50))  # Set ticks from -300 to 300 with a step of 100
    ax_in.set_xticklabels(['-300','-250',
                           '-200', '-150',
                           '-100', '-50',
                           '0', '50',
                           '100', '150',
                           '200', '250',
                           '300'])  # Custom labels without "mm"

    ax_in.set_ylabel("Y-Axis Position (mm)")

    # Set Y ticks with more intermediate steps
    ax_in.set_yticks(range(0, 300, 50))  # Set ticks from 0 to 120 with a step of 20
    ax_in.set_yticklabels(['20', '40', '60', '80', '100', '120'])  # Custom labels without "mm"

    # Set X and Y axis limits just in case
    ax_in.set_xlim([0, b_model.samples_per_axis])
    ax_in.set_ylim([0, b_model.samples_per_axis])

# Function to plot 2D magnetometer tracking coordinates
def plot_2d_coordinates():
    global canvas, ax, username, now, x_plot_values, y_plot_values, plot_after_id, sleep_time_ms

    csv_coordinates = get_csv_coordinates(username, now)

    # Check if the canvas and ax are already created
    if ax is None:
        # Step 1: Create a Matplotlib Figure and 2D Axes
        fig = Figure()
        ax = fig.add_subplot(111)

        # Step 2: Create a FigureCanvasTkAgg object
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    else:
        # Step 3: Clear the existing plot
        ax.cla()

    # Step 4: Extract magnetic magnitude numbers
    if len(csv_coordinates) >= 1:
        mag_x, mag_y, mag_z = csv_coordinates[-1] # last coordinate of the magnetometer magnitude to distance experiment

        # plot the tracking boundaries for reference
        ax.scatter(0,0, color='black', marker='+')
        ax.scatter(0, b_model.samples_per_axis, color='black', marker='+')
        ax.scatter(b_model.samples_per_axis, 0, color='black', marker='+')
        ax.scatter(b_model.samples_per_axis, b_model.samples_per_axis, color='black', marker='+')

        # Step 5: Convert the x and y magnitude to coordinates
        # check for the start_flag in the class
        if b_model.start_flag:
            # Calculate the starting coordinate based on the first magnetic field values
            b_model.get_initial_indexes(mag_x, mag_y)
            # Set the model off start
            b_model.start_flag = False
            # Plot the initial coordinates
            ax.scatter(b_model.initial_index_x, b_model.initial_index_y)
            print(f"start_flag: {b_model.start_flag}, initial x: {b_model.initial_index_x}, initial y: {b_model.initial_index_y}")

        else:
            # Get the next x and y coordinates based on new magnetometer information in 2D
            # This also primes for the next iteration
            b_model.get_next_index(mag_x, mag_y)

            # Plot the next calculated indexes
            # subtract b_model.samples_per_axis by b_model.next_index_x to flip the marker across the x axis
            ax.scatter(b_model.samples_per_axis - b_model.next_index_x,
                       b_model.next_index_y,
                       color='red', marker='+')

            # add the next data points to the plot array
            print(b_model.next_index_x, b_model.next_index_y)
            x_plot_values.append(b_model.next_index_x)
            y_plot_values.append(b_model.next_index_y)

            # add the line following the last 100 coordinates to the plot
            # use x_conversion to flip across the x-axis
            x_conversion = [b_model.samples_per_axis - x for x in x_plot_values[-150:]]
            ax.plot(x_conversion, y_plot_values[-150:])

    # Step 6: Draw the canvas
    try:
        setup_plot_range(ax)
        canvas.draw()
    except Exception as e:
        print(f"An error occurred while setting up the plot range: {e}")

    # Step 7: Cancel any existing scheduled call and schedule the next one
    if plot_after_id is not None:
        root.after_cancel(plot_after_id)

    # Schedule the next call after 500ms
    plot_after_id = root.after(sleep_time_ms, plot_2d_coordinates)


# Entry field function
def write_ble():
    #print(entryStr.get())
    output_string.set("Output: " + entryStr.get())


def read_file():
    global username, now, sleep_time_ms
    log_path = 'C:/Users/' + username + '/Downloads/' + now + '_ABALONE.csv'
    try:
        with open(log_path, 'r') as file:
            # Save the current scroll position
            current_scroll_position = text_widget.yview()

            content = file.read()
            text_widget.delete(1.0, tk.END)  # Clear the current content
            text_widget.insert(tk.END, content)  # Insert new content

            # Restore the scroll position
            text_widget.yview_moveto(current_scroll_position[0])
    except FileNotFoundError:
        text_widget.insert(tk.END, "File not found.")

    # Changed to 1ms for speed for the magnetometer magnitude to position experiment
    root.after(sleep_time_ms, read_file)  # Schedule the function to run again after 1000ms (1 second)


# Create the main window
root = tk.Tk()
root.title("3D Coordinates Plot")
root.geometry('800x400')

# Function to handle plot button click
def on_plot():
    """currently does nothing"""

# Create and pack the plot button using ttk
plot_button = ttk.Button(root, text="Plot 3D Coordinates", command=on_plot)
plot_button.pack()


# input field
input_frame = ttk.Frame(master = root)
entryStr = tk.StringVar()
entry = ttk.Entry(master = input_frame, textvariable = entryStr)
entry.pack(side = 'left', padx = 10)
button = ttk.Button(master = input_frame, text = 'Send', command = write_ble)
button.pack(side = 'left')
input_frame.pack(pady = 10)


# file read output
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=18)
text_widget.pack(side = 'right', padx=10, pady=10)


# output
output_string = tk.StringVar()
output_label = ttk.Label(
    master = root,
    text = 'Output',
    font = 'Calibri 12',
    textvariable = output_string)
output_label.pack(pady = 3)


# initialize the b_model class to allow for MATLAB interfacing
b_model = BModelClass()
b_model.abs_bound = 10
b_model.samples_per_axis = 301
b_model.grid_meter_range = 0.3
print("-> INITIALIZED: magnetic field object")
# create the dipole model with default settings
b_model.create_dipole_model()
print("-> INITIALIZED: magnetic field model")
# set this to True to note that you're starting on startup intialization
b_model.start_flag = True
# debugging print
print(f"-> DATA: start_flag: {b_model.start_flag}, next_x: {b_model.next_index_x}, next_y: {b_model.next_index_y}")


# Run the Tkinter event loop
read_file()
plot_2d_coordinates()
root.mainloop()