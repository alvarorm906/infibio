# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:42:54 2024

@author: uib
"""

import os

# Definir la carpeta de entrada y salida
carpeta_entrada = 'C:/Users/uib/Desktop/Experimentos/Experimentos homogeneizacion/SK1-HAP-DIP_2000_20240201'  # Cambia la ruta de acuerdo a tu caso
carpeta_salida = 'C:/Users/uib/Desktop/Experimentos/Experimentos homogeneizacion/SK1-HAP-DIP_2000_20240201'  # Cambia la ruta de acuerdo a tu caso

# Definir la dilución única
dilucion = 2000

# Inicializar el contador de tiempo y la replica actual
tiempo = 0
replica_actual = 1

# Iterar a través de los archivos en la carpeta de entrada
for nombre_archivo in sorted(os.listdir(carpeta_entrada)):
    # Construir el nuevo nombre del archivo
    nuevo_nombre = f"{dilucion}_{tiempo}_{replica_actual}.png"

    # Mostrar el nuevo nombre del archivo (opcional)
    print(nuevo_nombre)

    # Construir las rutas completas de entrada y salida
    ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)
    ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)

    # Cambiar el nombre del archivo (moverlo a la carpeta de salida)
    os.rename(ruta_entrada, ruta_salida)

    # Incrementar el contador de tiempo
    tiempo += 1

    # Si hemos alcanzado el límite de tiempos, reiniciar el contador de tiempo y cambiar a la siguiente replica
    if tiempo == 16:
        tiempo = 0
        replica_actual += 1

    # Si hemos alcanzado el límite de replicas, reiniciar el contador de replica y continuar con la siguiente iteración
    if replica_actual == 5:
        replica_actual = 1
