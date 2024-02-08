# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:48:54 2024

@author: uib
"""

import os

# Definir la carpeta de entrada y salida
carpeta_entrada = 'C:/Users/uib/Desktop/Experimentos/Experimentos homogeneizacion/SK1-SPOR_1000-5000_20240118'  # Cambia la ruta de acuerdo a tu caso
carpeta_salida = 'C:/Users/uib/Desktop/Experimentos/Experimentos homogeneizacion/SK1-SPOR_1000-5000_20240118'  # Cambia la ruta de acuerdo a tu caso

# Definir el diccionario de diluciones por letra de fila
diluciones_por_letra = {'A': 1000, 'B': 1000, 'C': 2000, 'D': 2000, 'E': 4000, 'F': 4000, 'G': 5000, 'H': 5000}

# Inicializar el contador y la fila actual
contador = 0
fila_actual = 'A'

# Iterar a través de los archivos en la carpeta de entrada
for nombre_archivo in sorted(os.listdir(carpeta_entrada)):
    # Obtener la letra de la fila y el número del pocillo
    letra_fila = fila_actual
    numero_pocillo = contador + 3

    # Obtener la dilución correspondiente a la letra de la fila
    dilucion = diluciones_por_letra[letra_fila]

    # Calcular el valor de Y
    valor_y = numero_pocillo - 3

    # Construir el nuevo nombre del archivo
    nuevo_nombre = f"{letra_fila}{numero_pocillo}_{dilucion}_{valor_y}.jpg"

    # Mostrar el nuevo nombre del archivo (opcional)
    print(nuevo_nombre)

    # Construir las rutas completas de entrada y salida
    ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)
    ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)

    # Cambiar el nombre del archivo (moverlo a la carpeta de salida)
    os.rename(ruta_entrada, ruta_salida)

    # Incrementar el contador
    contador += 1

    # Si hemos alcanzado el límite de pocillos por fila, reiniciar el contador y cambiar a la siguiente fila
    if contador == 8:
        contador = 0
        fila_actual = chr(ord(fila_actual) + 1)
