# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:03:26 2024

@author: uib
"""

import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from read_roi import read_roi_file
import shutil

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
carpeta_input = "C:/Users/uib/Desktop/prueba_script_python/prueba_zymoliasa/tiff"
carpeta_roi = None
ruta_csv = None

for files in os.walk(carpeta_input):
    carpeta_roi = os.path.join(carpeta_input, 'RoiSet')
    ruta_csv = os.path.join(carpeta_input, 'prueba_zymoliasa.csv')
    break

if carpeta_roi is None or ruta_csv is None:
    print("No se encontró ninguna carpeta 'RoiSet' o el archivo 'csv' en la carpeta de entrada.")
    exit()

df = pd.read_csv(ruta_csv, sep=';')

# Crear una carpeta para todos los gráficos
carpeta_graficos = os.path.join(carpeta_input, 'graficos')
os.makedirs(carpeta_graficos, exist_ok=True)

graficas_angulos_por_numero = {}
graficas_perfiles_por_numero = {}
    
        
# Iterar sobre los archivos en la carpeta de ROI
for roi_file in os.listdir(carpeta_roi):
    ruta_archivo_roi = os.path.join(carpeta_roi, roi_file)
    # Leer el archivo de ROI
    rois = read_roi_file(ruta_archivo_roi)
    
    # Procesar los datos del ROI
    for roi_name, roi_data in rois.items():
        # Obtener el número asociado al ROI
        numero_asociado = df.loc[df['LABEL'] == roi_name.split('.')[0], 'TRACK_ID'].iloc[0]
        
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
        plt.title(f"grafica_angulos_{numero_asociado}_{roi_name}")
        plt.savefig(os.path.join(carpeta_graficos, f"grafica_angulos_{numero_asociado}_{roi_name}.png"))
        plt.close(fig_angulos)
        
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
        plt.title(f"grafica_perfiles_{numero_asociado}_{roi_name}")
        plt.savefig(os.path.join(carpeta_graficos, f"grafica_perfiles_{numero_asociado}_{roi_name}.png"))
        # Almacenar las gráficas en diccionarios para la superposición
        if numero_asociado not in graficas_angulos_por_numero:
            graficas_angulos_por_numero[numero_asociado] = []
        graficas_angulos_por_numero[numero_asociado].append(fig_angulos)
        
        if numero_asociado not in graficas_perfiles_por_numero:
            graficas_perfiles_por_numero[numero_asociado] = []
        graficas_perfiles_por_numero[numero_asociado].append(fig_perfiles)


# Iterar sobre cada archivo en la carpeta de gráficos
for file_name in os.listdir(carpeta_graficos):
    # Obtener el ID del gráfico del nombre del archivo
    graph_id = file_name.split('_')[-1].split('.')[0]
    
    # Buscar el frame correspondiente en el DataFrame
    frame = df[df['LABEL'].str.contains(graph_id)]['FRAME'].values
    
    
    # Directorio donde se moverá el gráfico
    nuevo_dir = os.path.join(carpeta_graficos, f'frame_{frame}/')
    
    # Crear el directorio si no existe
    if not os.path.exists(nuevo_dir):
        os.makedirs(nuevo_dir)
    
    # Ruta completa del gráfico actual
    ruta_grafico = os.path.join(carpeta_graficos, file_name)
    
    # Ruta completa de la nueva ubicación del gráfico
    nueva_ruta_grafico = os.path.join(nuevo_dir, file_name)
    
    # Mover el gráfico al nuevo directorio
    shutil.move(ruta_grafico, nueva_ruta_grafico)
   
for numero_asociado, figuras in graficas_angulos_por_numero.items():
    fig_combinada_angulos = plt.figure()
    ax_angulos = fig_combinada_angulos.add_subplot(111, projection='polar')
    for fig in figuras:
        if fig.gca().lines:
            for line in fig.gca().lines:
                ax_angulos.plot(line.get_xdata(), line.get_ydata())
    plt.title(f"Gráficas de ángulos para número asociado {numero_asociado}")
    plt.savefig(os.path.join(carpeta_graficos, f"Gráficas de ángulos para número asociado {numero_asociado}.png"))
                
for numero_asociado, figuras in graficas_perfiles_por_numero.items():
    fig_combinada_perfiles = plt.figure()
    ax_perfiles = fig_combinada_perfiles.add_subplot(111)
    for fig in figuras:
        if fig.gca().lines:
            for line in fig.gca().lines:
                ax_perfiles.plot(line.get_xdata(), line.get_ydata())
    plt.title(f"Gráficas de perfiles para número asociado {numero_asociado}")
    plt.savefig(os.path.join(carpeta_graficos, f"Gráficas de perfiles para número asociado {numero_asociado}.png"))