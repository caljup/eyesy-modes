import pygame
from pygame import gfxdraw
import os
import math
import time
import random

def setup(screen, etc):
    global xr, yr
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    
    global screen_center, x, y, points
    screen_center = (xr // 2, yr // 2)
    x = screen_center[0]
    y = screen_center[1]
    points = [(x, y)]
    
    global spiral_angle_offset
    spiral_angle_offset = 0
    
    global colors, colors_list
    colors = {
        'magenta': (255, 0, 255),
        'cyan': (0, 255, 255),
        'yellow': (255, 255, 0),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'navy blue': (0, 0, 128),
        'royal purple': (148, 0, 211),
        'orange red': (255, 69, 0),
        'peach': (255, 218, 185),
        'light blue': (173, 216, 230),
        'pink': (255, 192, 203),
        'beige': (245, 245, 220),
        'lime green': (50, 205, 50),
        'turquoise': (64, 224, 208),
        'plum': (221, 160, 221),
        'maroon': (128, 0, 0),
        'evergreen': (0, 128, 0),
        'deep pink': (255, 20, 147),
        'lavender': (230, 230, 250),
        'silver': (192, 192, 192),
        'gold': (255, 215, 0),
        'forest green': (34, 139, 34),
        'sapphire': (102, 205, 170),
        'deep sky blue': (0, 191, 255),
        'tan': (210, 180, 140),
        'coral': (255, 127, 80),
        'salmon': (250, 128, 114),
        'indigo': (75, 0, 130),
        'olive': (128, 128, 0),
    }
    colors_list = list(colors.keys())
    
    global current_note
    current_note = etc.audio_in[0]
    
    global num_spirals, center_points
    num_spirals = 10
    center_points = generate_spiral_centers(num_spirals)
    
    global solid_colors
    solid_colors = []
    for _ in range(len(center_points)):
        color_key = random.choice(colors_list)
        solid_colors.append(colors[color_key])
        
    
    pygame.display.set_caption("Spiral Alley: The Uzumaki Story")
    pass


def draw(screen, etc):
    global x, y, points, num_spirals, current_note, center_points
    pygame.time.Clock().tick(45)
    
    bg_color = etc.color_picker_bg(etc.knob5)
    # color = etc.color_picker(etc.knob4)
    if etc.knob4 > 0.75:
        spiral_alley(screen, etc)
    elif etc.knob4 <= 0.75 and etc.knob4 > 0.5:
        if etc.audio_trig == True:
            center_points = generate_spiral_centers(num_spirals)
    elif etc.knob4 <= 0.5 and etc.knob4 > 0.25:
        for point, color in zip(center_points, solid_colors):
            x, y = point
            draw_spiral_line(screen, x, y, 1, etc, color)
    else:
        for _ in range(len(center_points)):
            x, y = center_points[_]
            color_key = random.choice(colors_list)
            color = colors[color_key]
            draw_spiral_line(screen, x, y, 1, etc, color)


def spiral_alley(screen, etc):
    num_of_spirals = 10
    alley_location = int(etc.knob3 * xr)
    left_alley_x = 0 + alley_location
    right_alley_x = xr - alley_location
    alley_height = yr
    height_diff = yr // num_of_spirals
    for _ in range(num_of_spirals):
        draw_spiral_line(screen, left_alley_x, alley_height, 1, etc, (0, 0, 0))
        draw_spiral_line(screen, right_alley_x, alley_height, 1, etc, (0, 0, 0))
        alley_height -= height_diff

def generate_spiral_centers(num_spirals):
    center_points = []
    for _ in range(num_spirals):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, xr)
        x = screen_center[0] + distance * math.cos(angle)
        y = screen_center[1] + distance * math.sin(angle)
        center_points.append((x, y))
    return center_points

def draw_spiral_line(screen, x, y, radius, etc, color):
    radius = radius + 1000 * etc.knob1
    global spiral_angle_offset
    spiral_angle_offset += 0.1 * etc.knob2
    base_num_points = 10000
    if spiral_angle_offset > 2 * math.pi:
        spiral_angle_offset = 0
    base_num_points = 10000
    num_points = int(base_num_points * etc.knob2 + 50)
    spiral_points = []
    for i in range(num_points):
        spiral_angle = -i * 0.1 + spiral_angle_offset
        r = radius + i * 0.1
        px = x + r * math.cos(spiral_angle)
        py = y + r * math.sin(spiral_angle)
        spiral_points.append((px, py))
    pygame.draw.lines(screen, color, False, spiral_points, 2)


