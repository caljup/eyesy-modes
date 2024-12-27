import pygame
import os
import math
import time

def setup(screen, etc):
    global xr, yr
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    pygame.display.set_caption("3D Pipelines")
    
    pass

def draw(screen, etc):
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up the pipe's properties
    pipe_radius = 50
    pipe_length = 1000
    pipe_segments = 20

    # Set up the rotation angles
    angle_x = 0
    angle_y = 0

    # Function to rotate 3D coordinates
    def rotate_x(x, y, z, angle):
        return x, y * math.cos(angle) - z * math.sin(angle), y * math.sin(angle) + z * math.cos(angle)

    def rotate_y(x, y, z, angle):
        return x * math.cos(angle) + z * math.sin(angle), y, -x * math.sin(angle) + z * math.cos(angle)

    for i in range(pipe_segments):
        # Calculate the 3D coordinates of the segment
        x = pipe_radius * math.cos(i * math.pi / pipe_segments)
        y = pipe_radius * math.sin(i * math.pi / pipe_segments)
        z = i * pipe_length / pipe_segments

        # Rotate the 3D coordinates
        x, y, z = rotate_x(x, y, z, angle_x)
        x, y, z = rotate_y(x, y, z, angle_y)

    # Project the 3D coordinates to 2D
    if 200 - z != 0:
        x = x * 200 / (200 - z)
        y = y * 200 / (200 - z)
    else:
        # Handle the case where z is equal to 200
        # You can either skip drawing this segment or handle it in a different way
        pass

        # Draw the segment as a 2D line
        pygame.draw.line(screen, (255, 255, 255), (screen_width / 2 + x, screen_height / 2 + y), (screen_width / 2 + x, screen_height / 2 + y + pipe_radius), 2)

    # Update the rotation angles
    angle_x += 0.01
    angle_y += 0.01

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(30)

