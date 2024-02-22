# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 12:02:31 2024

@author: uib
"""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import os
import pandas as pd
from read_roi import read_roi_file
from scipy.interpolate import interp1d

# Simulating the calculate_mass_center() function
def calculate_mass_center(x, y):
    x_center = np.mean(x)
    y_center = np.mean(y)
    return x_center, y_center

# Simulating the angles() function
def angles(x, y, x_center, y_center):
    x_rel = x - x_center
    y_rel = y - y_center
    r = np.sqrt(x_rel ** 2 + y_rel ** 2)
    theta = np.arctan2(y_rel, x_rel)
    return x_rel, y_rel, theta, r

# Path to the folder containing the ROI files
input_folder = "C:/Users/uib/Desktop/prueba_script_python/Exp_Zymolyase01-005_ConA03-2024110/E1/0/tiff"
roi_folder = os.path.join(input_folder, 'RoiSet')
roi_list = os.listdir(roi_folder)
csv_path = os.path.join(input_folder, 'export.csv')
df = pd.read_csv(csv_path, skiprows=range(1, 4))
roi_name = roi_list[9]
roi_data = read_roi_file(os.path.join(roi_folder, roi_list[9]))
# Get the number associated with the ROI
associated_number = df.loc[df['LABEL'] == roi_name.split('.')[0], 'TRACK_ID'].iloc[0]

x = np.array(roi_data[roi_name.split('.')[0]]['x'], dtype=np.float32)
y = np.array(roi_data[roi_name.split('.')[0]]['y'], dtype=np.float32)

# Smooth the data using lowess
smoothed_y = lowess(y, range(len(x)), frac=0.1)
smoothed_x = lowess(x, range(len(x)), frac=0.1)
# Interpolate the smoothed curve with a third order interpolation
interp_func_y = interp1d(smoothed_y[:, 0], smoothed_y[:, 1], kind='cubic')
interp_func_x = interp1d(smoothed_x[:, 0], smoothed_x[:, 1], kind='cubic')


# Define equally spaced x-values
x_values_equally_spaced = np.linspace(min(smoothed_y[:, 0]), max(smoothed_y[:, 0]), len(x))
# Calculate corresponding y-values using interpolation
y_values_equally_spaced = interp_func_y(x_values_equally_spaced)
x_values_equally_spaced = interp_func_x(x_values_equally_spaced)
# Plotting
plt.figure(figsize=(8, 6))
plt.plot(y, 'o', label='Original Data')
plt.plot(smoothed_y[:, 1], 'r-', label='Lowess Smoothed')
plt.plot(y_values_equally_spaced, 'g--', label='Equally Spaced Interpolation')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Lowess Smoothing and Equally Spaced Interpolation')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(x, 'o', label='Original Data')
plt.plot(smoothed_x[:, 1], 'r-', label='Lowess Smoothed')
plt.plot(x_values_equally_spaced, 'g--', label='Equally Spaced Interpolation')
plt.legend()
plt.xlabel('X')
plt.ylabel('X')
plt.title('Lowess Smoothing and Equally Spaced Interpolation')
plt.grid(True)
plt.show()



## Let's calculate the curvature of the interpolated plot

# To calculate the curvature of the original shape of the yeast, let's create a joined array
xy_array = [[x_val, y_val] for x_val, y_val in zip(x_values_equally_spaced, y_values_equally_spaced)]
# Compute second derivative using finite differences
second_derivative_y = np.gradient(np.gradient(y_values_equally_spaced))
second_derivative_x = np.gradient(np.gradient(x_values_equally_spaced))
# Compute curvature as  curvature = np.abs(second_derivative) / (1 + first_derivative**2)**(3/2)
curvature_y = second_derivative_y/ (1 + np.gradient(y_values_equally_spaced)**2)**(3/2)
curvature_x = second_derivative_x/ (1 + np.gradient(x_values_equally_spaced)**2)**(3/2)


# Plot second derivatives
plt.figure(figsize=(8, 6))
plt.plot(curvature_y, 'b-', label='Curvature (Y)')
plt.xlabel('X')
plt.ylabel('Curvature')
plt.title('Curvature for Y')
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(curvature_x,  'b-', label='Curvature (X)')
plt.xlabel('X')
plt.ylabel('Curvature')
plt.title('Curvature for X')
plt.grid(True)
plt.legend()
plt.show()


# Convert to numpy array for easier manipulation
xy_array = np.array(xy_array)

# Compute second derivative using finite differences
dx = np.gradient(xy_array[:, 0])
dy = np.gradient(xy_array[:, 1])
d2x = np.gradient(dx)
d2y = np.gradient(dy)

# Compute curvature as 
curvature = (dx * d2y - dy * d2x) / ((dx**2 + dy**2)**(3/2))

# Plot curvature
plt.figure(figsize=(8, 6))
plt.plot(curvature, 'b-', label='Curvature')
plt.xlabel('Index')
plt.ylabel('Curvature')
plt.title('Curvature Plot')
plt.grid(True)
plt.legend()
plt.show()
plt.figure(figsize=(8, 6))
plt.plot(x,y,  'b-', label='Curvature (X)')
plt.xlabel('X')
plt.ylabel('Curvature')
plt.title('Curvature for X')
plt.grid(True)
plt.legend()
plt.show()