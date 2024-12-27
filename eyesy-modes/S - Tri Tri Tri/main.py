import pygame
from pygame import gfxdraw
import os
import math
import time

def setup(screen, etc):
    global xr, yr
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    pygame.display.set_caption("Triangle Scatter")
    pass

class PhaseIncrementor:
    def __init__(self):
        self.circle_points = [0, math.pi / 2, math.pi, (3 * math.pi) / 2 ]
        self.phase_increment = 0.1
        
    def reset(self):
        self.circle_points = [0, math.pi / 2, math.pi, (3 * math.pi) / 2 ]
        
    def increment(self, val):
        if self.circle_points[0] > 2 * math.pi:
            self.reset()
            pass
        increment = self.phase_increment * float(val)
        for x, y in enumerate(self.circle_points):
            new_position = y + increment
            self.circle_points[x] = new_position        
        return self.circle_points
        
def draw_triangle(surface, color, pos1, pos2, pos3):
    pygame.draw.polygon(surface, color, [pos1, pos2, pos3], 0)
    
def create_triangle(screen, color, bg_color, x_offset, y_offset, triangle_center):
    x_inner_offset = x_offset * 0.9
    y_inner_offset = y_offset * 0.9
    
    inner_triangle = [(triangle_center[0], triangle_center[1] - y_inner_offset), 
                       (triangle_center[0] - x_inner_offset, triangle_center[1] + y_inner_offset), 
                       (triangle_center[0] + x_inner_offset, triangle_center[1] + y_inner_offset)]
    
    outer_triangle = [(triangle_center[0], triangle_center[1] - y_offset),
                      (triangle_center[0] - x_offset, triangle_center[1] + y_offset),
                      (triangle_center[0] + x_offset, triangle_center[1] + y_offset)]
    
    draw_triangle(screen, color, *outer_triangle)
    draw_triangle(screen, bg_color, *inner_triangle)
    
    return None
    
def tri(screen, screen_center, color, bg_color, x_offset, y_offset, num_of_triangles, radius, phase_points):
    for x in range(num_of_triangles, 1, -1):
        rc = radius * x * 0.5
        
        if x % 3 == 0:
            x_center = int(screen_center[0] + rc * math.cos(phase_points[0]))
            y_center = int(screen_center[1] + rc * math.sin(phase_points[0]))
            triangle_center = (x_center, y_center)
            create_triangle(screen, color, bg_color, x_offset, y_offset, triangle_center)
        else:
            x_center = int(screen_center[0] + rc * math.cos(phase_points[3]))
            y_center = int(screen_center[1] + rc * math.sin(phase_points[3]))
            triangle_center = (x_center, y_center)
            create_triangle(screen, color, bg_color, x_offset, y_offset, triangle_center)
        
        if x % 2 == 0:
            extra = radius * math.exp(phase_points[0] / 2)
            x_center = int(screen_center[0] + rc * math.sin(phase_points[2])) + extra
            y_center = int(screen_center[1] + rc * math.cos(phase_points[2]))
            triangle_center = (x_center, y_center)
            create_triangle(screen, color, bg_color, x_offset, y_offset, triangle_center)
        else:
            x_center = int(screen_center[0] + rc * math.sin(phase_points[1]))
            y_center = int(screen_center[1] + rc * math.cos(phase_points[1]))
            triangle_center = (x_center, y_center)
            create_triangle(screen, color, bg_color, x_offset, y_offset, triangle_center)
    
    create_triangle(screen, color, bg_color, x_offset, y_offset, screen_center)


phaseIncrementor = PhaseIncrementor()

def draw(screen, etc):
    pygame.time.Clock().tick(30)
    screen_center = (xr // 2, yr // 2)
    bg_color = etc.color_picker_bg(etc.knob5)
    color = etc.color_picker(etc.knob4)
    x_offset = 200 * etc.knob2
    y_offset = 200 * etc.knob2
    radius = 300 * etc.knob2
    # Simulate audio input: Random scatter amount
    scatter_amount = etc.audio_in[0] /100  # Adjust range as needed
    phase_points = phaseIncrementor.increment(etc.knob1)
    num_of_triangles = int(etc.knob3 * 50)
    
    tri(screen, screen_center, color, bg_color, x_offset, y_offset, num_of_triangles, radius, phase_points)

