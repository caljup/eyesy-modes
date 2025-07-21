import pygame
import math

def setup(screen, eyesy):
    global pipe_points, camera_x, camera_y, camera_z
    pipe_points = []
    for i in range(100):
        x = i * 10
        y = math.sin(i / 10.0) * 100
        z = i
        pipe_points.append((x, y, z))
    camera_x, camera_y, camera_z = 0, 0, -200

def draw(screen, eyesy):
    global pipe_points, camera_x, camera_y, camera_z
    screen.fill((0, 0, 0))
    camera_x += eyesy.knob1 * 10
    camera_y += eyesy.knob2 * 10
    camera_z += eyesy.knob3 * 10
    for i in range(len(pipe_points) - 1):
        x1, y1, z1 = pipe_points[i]
        x2, y2, z2 = pipe_points[i + 1]
        x1_2d = int(x1 + camera_x) + eyesy.xres / 2
        y1_2d = int(-y1 + camera_y) + eyesy.yres / 2
        x2_2d = int(x2 + camera_x) + eyesy.xres / 2
        y2_2d = int(-y2 + camera_y) + eyesy.yres / 2
        pygame.draw.line(screen, (255, 255, 255), (x1_2d, y1_2d), (x2_2d, y2_2d), 2)