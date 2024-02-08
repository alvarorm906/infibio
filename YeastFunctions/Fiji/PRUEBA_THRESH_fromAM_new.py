# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:43:51 2023

@author: anusk
DIRECCIONES
"""
import cv2
from skimage.morphology import closing, square
import numpy as np
from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.cm as cmap
from skimage.draw import polygon_perimeter
from skimage.color import rgb2gray
#from scipy.ftt import fft

class Directions(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


NORTH = Directions.NORTH
EAST = Directions.EAST
SOUTH = Directions.SOUTH
WEST = Directions.WEST

def trace_boundary(image):
    padded_img = np.pad(image, 1)

    img = padded_img[1:-1, 1:-1]
    img_north = padded_img[:-2, 1:-1]
    img_south = padded_img[2:, 1:-1]
    img_east = padded_img[1:-1, 2:]
    img_west = padded_img[1:-1, :-2]

    border = np.zeros((4, *padded_img.shape), dtype=np.intp)

    border[NORTH][1:-1, 1:-1] = (img == 1) & (img_north == 0)
    border[EAST][1:-1, 1:-1] = (img == 1) & (img_east == 0)
    border[SOUTH][1:-1, 1:-1] = (img == 1) & (img_south == 0)
    border[WEST][1:-1, 1:-1] = (img == 1) & (img_west == 0)

    adjacent = np.zeros((4, *image.shape), dtype=np.intp)
    adjacent[NORTH] = np.argmax(np.stack(
        (border[WEST][:-2, 2:],
         border[NORTH][1:-1, 2:],
         border[EAST][1:-1, 1:-1])
    ), axis=0)
    adjacent[EAST] = np.argmax(np.stack(
        (border[NORTH][2:, 2:],
         border[EAST][2:, 1:-1],
         border[SOUTH][1:-1, 1:-1])
    ), axis=0)
    adjacent[SOUTH] = np.argmax(np.stack(
        (border[EAST][2:, :-2],
         border[SOUTH][1:-1, :-2],
         border[WEST][1:-1, 1:-1])
    ), axis=0)
    adjacent[WEST] = np.argmax(np.stack(
        (border[SOUTH][:-2, :-2],
         border[WEST][:-2, 1:-1],
         border[NORTH][1:-1, 1:-1])
    ), axis=0)

    directions = np.zeros((len(Directions), *image.shape, 3, 3), dtype=np.intp)
    directions[NORTH][..., :] = [(3, -1, 1), (0, 0, 1), (1, 0, 0)]
    directions[EAST][..., :] = [(-1, 1, 1), (0, 1, 0), (1, 0, 0)]
    directions[SOUTH][..., :] = [(-1, 1, -1), (0, 0, -1), (1, 0, 0)]
    directions[WEST][..., :] = [(-1, -1, -1), (0, -1, 0), (-3, 0, 0)]

    proceding_edge = directions[
        np.arange(len(Directions))[:, np.newaxis, np.newaxis],
        np.arange(image.shape[0])[np.newaxis, :, np.newaxis],
        np.arange(image.shape[1])[np.newaxis, np.newaxis, :],
        adjacent
    ]

    unprocessed_border = border[:, 1:-1, 1:-1].copy()
    borders = list()
    for start_pos in zip(*np.nonzero(unprocessed_border)):
        if not unprocessed_border[start_pos]:
            continue

        idx = len(borders)
        borders.append(list())
        start_arr = np.array(start_pos, dtype=np.intp)
        current_pos = start_arr
        while True:
            unprocessed_border[tuple(current_pos)] = 0
            borders[idx].append(tuple(current_pos[1:]))
            current_pos += proceding_edge[tuple(current_pos)]
            if np.all(current_pos == np.array(start_pos)):
                break

    # match np.nonzero style output
    border_pos = list()
    for border in borders:
        border = np.array(border)
        border_pos.append([border[:, 0], border[:, 1]])

    return border_pos

path_v = r'C:/Users/xisca/Desktop/Microscopy/04-04-2023/4_1_variance.png'
image_rgb = cv2.imread(path_v)
image_1 = rgb2gray(image_rgb)
image = (image_1*255).astype(np.uint8)
path_t = r'C:/Users/xisca/Desktop/Microscopy/04-04-2023/4_1_threshold.png'
thresh_rgb = cv2.imread(path_t)
thresh_1  = rgb2gray(thresh_rgb).astype('uint8')
thresh = (thresh_1*255).astype(np.uint8)
bw = closing(image > thresh, square(3))

borders = trace_boundary(bw)

img = np.stack([image] * 3, axis=-1)
for idx, border in enumerate(borders):
    # demonstrate that pixels are in order
    rr_bord, cc_bord = border
    rr, cc = polygon_perimeter(rr_bord, cc_bord)

    # rainbow *_*
    col_idx = idx * (1337 + 42000) % len(borders)

    color = np.array(cmap.gist_rainbow(1. * col_idx / len(borders))) * 255
    img[rr, cc, :] = color[:-1]
    
plt.imshow(img)
plt.gca().axis("off")
plt.show()

def calculate_mass_center(x_coords, y_coords):
    total_mass = 0
    x_mass_sum = 0
    y_mass_sum = 0
    
    for i in range(len(x_coords)):
        mass = 1  # assume unit mass for each point
        total_mass += mass
        x_mass_sum += mass * x_coords[i]
        y_mass_sum += mass * y_coords[i]
    
    x_center = x_mass_sum / total_mass
    y_center = y_mass_sum / total_mass
    
    return x_center, y_center

def angulos(x, y, x_center, y_center):
    x_a = np.array(x)
    y_a = np.array(y)
    x_c = x_center*np.ones(len(x))
    y_c = y_center*np.ones(len(y))
    x_rel = x_a - x_c
    y_rel = y_a - y_c
    r = np.sqrt(x_rel**2 + y_rel**2) #distancia de cada punto al centro de masas
    theta = np.arctan2(y_rel, x_rel)
    return x_c, y_c, theta, r, y_rel, x_rel


#for i in range(len(borders)): #solo usar cuando todos los contornos sean validos
for i in ([4, 10, 15]):
    x_center, y_center = calculate_mass_center(borders[i][1], borders[i][0])
    x_c, y_c, theta, r, y_rel, x_rel = angulos(borders[i][1], borders[i][0], x_center, y_center)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.scatter(theta, r, s = 3)
    plt.show()
"""    
def parametrizacion():
    for i in ([4, 10, 15]):

        L = np.arange(0, len(borders[i][0]))
        plt.plot(L, borders[i][0], label = 'x(L)')
        plt.plot(L, borders[i][1], label = 'y(L)')
        plt.legend()
        plt.xlabel('pixel')
        plt.ylabel('x,y')
        plt.show()
    return       
parametrizacion()
"""
for i in ([4, 10, 15]):

    L = np.arange(0, len(borders[i][0]))
    #Calculamos la media de cada serie de datos y se la restamos
    m_x = np.mean(borders[i][0])
    x = borders[i][0] - m_x*np.ones(len(borders[i][0]))
    m_y = np.mean(borders[i][1])
    y = borders[i][1] - m_y*np.ones(len(borders[i][1]))
    plt.plot(L, x, label = 'x(L)')
    plt.plot(L, y, label = 'y(L)')
    plt.legend()
    plt.xlabel('pixel')
    plt.ylabel('x,y')
    plt.show()
    """
    # a partir de aqui plotear los coef
    x = borders[i][0]
    x_ft = fft(x)
    """    
