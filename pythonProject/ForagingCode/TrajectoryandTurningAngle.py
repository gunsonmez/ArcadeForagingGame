import numpy as np
import math
import matplotlib.pyplot as plt
import os


def absolute_angle_between_points(p1, p2):  # Function to calculate angle between two points(absolute value)
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    if d1 == 0 or d2 == 0:
        deg = 0
    else:
        deg = abs(math.atan2(d2, d1)) / math.pi * 180

    return deg


def mean_turning_angle(
        file_name):  # Calculate the sum of all angles between consecutive locations and
    # divide it to step number to find the average
    data_array = np.load(file_name)  # Load the saved array
    duration = data_array[:, 0]  # First column for time data
    xy_pos = data_array[:, [1, 2]]  # 2nd and 3rd columns for x, y positions
    angle_sum = 0

    for i in range(len(duration)):
        if i < len(duration) - 1:
            angle_sum += absolute_angle_between_points(xy_pos[i], xy_pos[i + 1])

    angle_mean = angle_sum / (len(duration) - 1)

    return angle_mean

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def show_trajectory_and_mean(file_name):  # Function to search the directory, find all .npy files and
    # to create a trajectory plot for each file

    mean_angle = mean_turning_angle(file_name)  # Find mean angle
    image_format = "png"  # Save format for plots
    data_array = np.load(filename)

    duration = data_array[:, 0]
    x_pos = data_array[:, 1]
    y_pos = data_array[:, 2]

    plt.plot(x_pos[0], y_pos[0], "ko")  # Starting point, black dot
    plt.scatter(x_pos, y_pos, s=0.5,  c=duration, cmap="plasma")
    plt.plot(x_pos[-1], y_pos[-1], "ro")  # Ending point, red dot
    plt.xlim(0, SCREEN_WIDTH)
    plt.ylim(0, SCREEN_HEIGHT)
    save_title = "Plots/" + filename.replace("npy", image_format)  # Define the plot title
    plt.title(save_title)
    plt.xlabel(f"Mean turning angle = {mean_angle}")  # Display mean angle on plot
    # plt.show()
    plt.savefig(save_title)  # Save plot to directory
    plt.clf()  # Close the figure to prevent overwriting plots


# Search the directory for .npy files and put them through the plot function
root_dir = os.path.dirname(os.path.abspath(__file__))
extension = ('.npy')

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extension:
            filename = os.path.basename(file)
            show_trajectory_and_mean(filename)
