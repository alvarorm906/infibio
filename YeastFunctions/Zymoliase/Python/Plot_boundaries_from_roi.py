# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:37:04 2024

@author: uib
"""
import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from read_roi import read_roi_file

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
carpeta_roi = "C:/Users/uib/Desktop/RoiSet"
ruta_csv = "C:/Users/uib/Desktop/export.csv"
df = pd.read_csv(ruta_csv)
graficas_angulos_por_numero = {}
graficas_perfiles_por_numero = {}

# Iterar sobre los archivos en la carpeta de ROI
for file in os.listdir(carpeta_roi):
    # Construir la ruta completa del archivo de ROI
    ruta_archivo_roi = os.path.join(carpeta_roi, file)
    
    # Leer el archivo de ROI
    rois = read_roi_file(ruta_archivo_roi)
    
    # Procesar los datos del ROI
    for roi_name, roi_data in rois.items():
        # Obtener el número asociado al ROI
        numero_asociado = df.loc[df['LABEL'] == roi_name, 'TRACK_ID'].iloc[0]
        
        # Obtener las coordenadas x e y del ROI
        x = np.array(roi_data['x'])
        y = np.array(roi_data['y'])
        
        # Calcular el centro de masa
        x_center, y_center = calculate_mass_center(x, y)

        # Generar gráfica de ángulos polares
        fig_angulos = plt.figure()
        ax_angulos = fig_angulos.add_subplot(111, projection='polar')
        x_rel, y_rel, theta, r = angulos(x, y, x_center, y_center)
        ax_angulos.plot(theta, r, '-')
        plt.title(f"{numero_asociado}_{roi_name}")
        plt.show()

        # Generar gráfica de perfiles
        fig_perfiles = plt.figure()
        ax_perfiles = fig_perfiles.add_subplot(111)
        L = np.arange(0, len(x))
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        x = x - x_mean
        y = y - y_mean
        ax_perfiles.plot(L, x, label='x(L)')
        ax_perfiles.plot(L, y, label='y(L)')
        ax_perfiles.legend()
        plt.title(f"{numero_asociado}_{roi_name}")
        plt.show()

        # Almacenar las gráficas en diccionarios para la superposición
        if numero_asociado not in graficas_angulos_por_numero:
            graficas_angulos_por_numero[numero_asociado] = []
        graficas_angulos_por_numero[numero_asociado].append(fig_angulos)
        
        if numero_asociado not in graficas_perfiles_por_numero:
            graficas_perfiles_por_numero[numero_asociado] = []
        graficas_perfiles_por_numero[numero_asociado].append(fig_perfiles)



for numero_asociado, figuras in graficas_angulos_por_numero.items():
    fig_combinada_angulos = plt.figure()
    ax_angulos = fig_combinada_angulos.add_subplot(111, projection='polar')
    for fig in figuras:
        if fig.gca().lines:
            for line in fig.gca().lines:
                ax_angulos.plot(line.get_xdata(), line.get_ydata())
    plt.title(f"Gráficas de ángulos para número asociado {numero_asociado}")
    plt.show()



for numero_asociado, figuras in graficas_perfiles_por_numero.items():
    fig_combinada_perfiles = plt.figure()
    ax_perfiles = fig_combinada_perfiles.add_subplot(111)
    for fig in figuras:
        if fig.gca().lines:
            for line in fig.gca().lines:
                ax_perfiles.plot(line.get_xdata(), line.get_ydata())

    plt.title(f"Gráficas de perfiles para número asociado {numero_asociado}")
    plt.show()




