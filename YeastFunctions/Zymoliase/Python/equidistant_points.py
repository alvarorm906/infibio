# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:08:40 2024

@author: uib
"""
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import os
import pandas as pd
from read_roi import read_roi_file
from scipy.integrate import trapz

# Simulando la función calculate_mass_center()
def calculate_mass_center(x, y):
    x_center = np.mean(x)
    y_center = np.mean(y)
    return x_center, y_center

# Simulando la función angulos()
def angulos(x, y, x_center, y_center):
    x_rel = x - x_center
    y_rel = y - y_center
    r = np.sqrt(x_rel ** 2 + y_rel ** 2)
    theta = np.arctan2(y_rel, x_rel)
    return x_rel, y_rel, theta, r


# Ruta a la carpeta que contiene los archivos de ROI
carpeta_input = "C:/Users/uib/Desktop/prueba_script_python/Exp_Zymolyase01-005_ConA03-2024110/E1/0/tiff"
carpeta_roi = os.path.join(carpeta_input, 'RoiSet')
lista_roi = os.listdir(carpeta_roi)
ruta_csv = os.path.join(carpeta_input, 'export.csv')
df = pd.read_csv(ruta_csv, skiprows=range(1, 4))
roi_name = lista_roi[9]
roi_data = read_roi_file(os.path.join(carpeta_roi, lista_roi[9]))
 # Obtener el número asociado al ROI
numero_asociado = df.loc[df['LABEL'] == roi_name.split('.')[0], 'TRACK_ID'].iloc[0]

x = np.array(roi_data[roi_name.split('.')[0]]['x'], dtype=np.float32)
y = np.array(roi_data[roi_name.split('.')[0]]['y'], dtype=np.float32)
# Plot the image as an xy plot
plt.plot(x, y, 'o-')  # 'o-' represents a line with markers at each point
plt.xlabel('X')  # Label for the x-axis
plt.ylabel('Y')  # Label for the y-axis
plt.title('XY Plot')  # Title of the plot
plt.grid(True)  # Show grid
plt.show()
# Calcular el centro de masa
x_center, y_center = calculate_mass_center(x, y)

# Centrar los datos
x_mean = np.mean(x)
y_mean = np.mean(y)
x = x - x_mean
y = y - y_mean

# Aplicar suavizado utilizando un promedio móvil
# Ajustar el tamaño de la ventana para un perfil más suave o más rugoso
smoothed_x = lowess(x, range(len(x)), frac=0.1, return_sorted=False)
smoothed_y = lowess(y, range(len(y)), frac=0.1, return_sorted=False)
smoothed_x = np.append(smoothed_x, smoothed_x[-1])
smoothed_y = np.append(smoothed_y, smoothed_y[-1])
# Plot the image as an xy plot
plt.plot(smoothed_x, smoothed_y, 'o-')  # 'o-' represents a line with markers at each point
plt.xlabel('X')  # Label for the x-axis
plt.ylabel('Y')  # Label for the y-axis
plt.title('XY Plot')  # Title of the plot
plt.grid(True)  # Show grid
plt.show()
# Calcular los ángulos polares
x_rel, y_rel, theta, r = angulos(smoothed_x, smoothed_y, x_center, y_center)

# Calcular la distancia acumulada s
s = np.cumsum(np.sqrt(np.diff(x_rel)**2 + np.diff(y_rel)**2))
s = np.insert(s, 0, 0)  # Agregar el punto inicial en s

# Calcular la integral de cos(theta)*sin(theta) con respecto a s
integral = trapz(np.cos(theta)*np.sin(theta), s)

# Calcular la media de X (mean(X))
mean_X = np.mean(x)  # Utilizamos x para la media de X, ajusta según sea necesario

# Calcular el resultado final
resultado = mean_X + integral

print("El resultado para", roi_name, "es:", resultado)

# Mostrar la gráfica de los ángulos polares
fig_integral, ax_integral = plt.subplots()
ax_integral.plot(s, np.cos(theta) * np.sin(theta), label='Integrando función')
ax_integral.set_title('Integral de cos(theta)*sin(theta)')
ax_integral.set_xlabel('Distancia acumulada (s)')
ax_integral.set_ylabel('Valor de la función')
ax_integral.legend()
plt.show()

def calculate_equidistant_points(x, y, n):
    """
    Calculate equidistant points along a curve defined by x and y coordinates.

    Parameters:
        x (array-like): x-coordinates of the curve.
        y (array-like): y-coordinates of the curve.
        n (int): Number of equidistant points desired.

    Returns:
        equidistant_points (ndarray): Array containing the equidistant points along the curve.
    """
    
    # Add the last point again to close the curve
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    
    # Calculate the total length of the curve
    total_length = np.sum(np.sqrt((np.roll(x, -1) - x)**2 + (np.roll(y, -1) - y)**2))
    
    # Calculate the interval length
    interval_length = total_length / (n-1)
    
    # Initialize the equidistant points array
    equidistant_points = np.zeros((n, 2))
     
     
    # Find equidistant points
    accumulated_length = 0
    for i in range(1,n):
        accumulated_length += interval_length
        
        # Find the corresponding x value using interpolation
        target_length = accumulated_length
        current_length = 0
        j = 1
        while j < len(x)-1 and current_length < target_length:
            current_length += np.sqrt((x[j] - x[j-1])**2 + (y[j] - y[j-1])**2)
            j += 1
    
        # Interpolate to find y value corresponding to the x value
        # Explanation of normalization step:
        # The following division normalizes the interpolated distance to be within the unit vector between the previous point and the current point.
        # It scales the interpolated distance relative to the total distance between the two points, ensuring that the interpolation is consistent
        # regardless of the magnitude of the original vector between the points.
        equidistant_points[i] = [x[j-1] + (x[j] - x[j-1]) * (target_length - (current_length - np.sqrt((x[j] - x[j-1])**2 + (y[j] - y[j-1])**2)))/(np.sqrt((x[j] - x[j-1])**2 + (y[j] - y[j-1])**2)), 
                                 y[j-1] + (y[j] - y[j-1]) * (target_length - (current_length - np.sqrt((x[j] - x[j-1])**2 + (y[j] - y[j-1])**2)))/(np.sqrt((x[j] - x[j-1])**2 + (y[j] - y[j-1])**2))]
    
    # Plot the original curve
    plt.plot(x, y, label='Original Curve')
    # Plot the equidistant points
    plt.scatter(equidistant_points[:, 0], equidistant_points[:, 1], color='red', label='Equidistant Points')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Original Curve with Equidistant Points')
    plt.legend()
    plt.grid(True)
    plt.show()
    return equidistant_points

# Example usage:
# x and y are the recalculated positions using lowess
# n is the number of equidistant points you want to calculate
# equidistant_points = calculate_equidistant_points(x, y, n)
# Plotting the original curve and equidistant points
calculate_equidistant_points(smoothed_x, smoothed_y, 60)
