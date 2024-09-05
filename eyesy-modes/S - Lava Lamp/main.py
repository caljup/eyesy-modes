# import pygame
# import random
# import math
# #Give the user ability to change what which lava lamp style they go with

# # Define Lava class
# class Lava:
#     def __init__(self, x, y, radius, vel_x, vel_y):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.vel_x = vel_x
#         self.vel_y = vel_y
#         self.color = lava_color
        
#     def update(self):
#         # Apply gravity
#         self.vel_y += 0.05
        
#         # Apply viscosity
#         self.vel_x *= 0.99
#         self.vel_y *= 0.99
        
#         # Update position
#         self.x += self.vel_x
#         self.y += self.vel_y
        
#         # Apply friction
#         self.vel_x = 0.95
#         self.vel_y = 0.95
        
#         # Bounce off window edges
#         if self.x < self.radius or self.x > WIDTH - self.radius:
#             self.vel_x *= -1
#         if self.y < self.radius or self.y > HEIGHT - self.radius:
#             self.vel_y *= -1

#     def draw(self):
#         pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# def setup(etc, screen):
#     global xr, yr, initial_height
#     # xr = etc.x_res
#     # yr = etc.y_res
#     xr = 1280
#     yr = 720
#     initial_height = yr
#     pass


# # Randomly divide the lava into smaller goops
# def divide_lava(lava):
#     divided_lava = []
#     num_pieces = random.randint(2, 4)
#     for _ in range(num_pieces):
#         radius = random.randint(MIN_RADIUS, lava.radius - 10)
#         vel_x = random.uniform(-MAX_SPEED, MAX_SPEED)
#         vel_y = random.uniform(-MAX_SPEED, MAX_SPEED)
#         divided_lava.append(Lava(lava.x, lava.y, radius, vel_x, vel_y))
#     return divided_lava


# # Combine smaller goops into larger goops
# def combine_lava(lava_pieces):
#     combined_lava = []
#     num_pieces = len(lava_pieces)
#     if num_pieces < 2:
#         return lava_pieces
    
#     combined_radius = sum(p.radius for p in lava_pieces)
#     average_x = sum(p.x for p in lava_pieces) / num_pieces
#     average_y = sum(p.y for p in lava_pieces) / num_pieces
    
#     max_speed = max(MAX_SPEED for p in lava_pieces)
    
#     combined_lava.append(Lava(average_x, average_y, combined_radius, random.uniform(-max_speed, max_speed),
#                              random.uniform(-max_speed, max_speed)))
    
#     return combined_lava
  
# def draw(etc, screen):
#     global xr, yr, initial_height
    

#     pass

# if __name__ == "__main__":

#     pygame.init()
#     screen = pygame.display.set_mode((1280, 720))
#     pygame.display.set_caption("Lava Lamp Simulation")
#     clock = pygame.time.Clock()
#     running = True
#     etc = "etc"
#     setup(etc, screen)
#     white = (255, 255, 255)
#     background_color = (255, 255, 255)
#     lava_color = (255, 0, 0)
#     HEIGHT = 800
#     WIDTH = 600
#     # Define constants
#     MAX_RADIUS = 80
#     MIN_RADIUS = 20
#     MAX_SPEED = 3
    
#     # Create Lava objects
#     lava_list = []
#     num_lava = 8
#     for _ in range(num_lava):
#         x = random.randint(100, WIDTH - 100)
#         y = random.randint(100, HEIGHT - 100)
#         radius = random.randint(MIN_RADIUS, MAX_RADIUS)
#         vel_x = random.uniform(-MAX_SPEED, MAX_SPEED)
#         vel_y = random.uniform(-MAX_SPEED, MAX_SPEED)
#         lava_list.append(Lava(x, y, radius, vel_x, vel_y))

    
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
        
#         for i, lava in enumerate(lava_list):
#            lava.update()
        
#         # Check for merging
#         for other_lava in lava_list[i+1:]:
#             if math.hypot(lava.x - other_lava.x, lava.y - other_lava.y) <= (lava.radius + other_lava.radius):
#                 combined_lava = divide_lava(lava) + divide_lava(other_lava)
#                 lava_list.remove(lava)
#                 lava_list.remove(other_lava)
#                 lava_list.extend(combine_lava(combined_lava))
        
#         screen.fill(background_color)
        
#         for lava in lava_list:
#             lava.draw()
        
#         # draw(etc, screen)
        
#         pygame.display.flip()
#         clock.tick(60)

import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Transforming Blob Object")
clock = pygame.time.Clock()

def create_blob(N, time):
    amps = np.random.uniform(0, 1 / (2 * N), N)
    phases = np.random.uniform(0, 2 * np.pi, N)

    alpha = np.linspace(0, 2 * np.pi, 1000)
    radius = 1 + np.sum(amps[i] * np.cos((i+1) * alpha + phases[i]) for i in range(N))  # Fixed radius calculation
    x = np.cos(alpha) * radius
    y = np.sin(alpha) * radius

    return x, y

def draw_blob(x, y):
    for i in range(len(x) - 1):
        pygame.draw.line(screen, (255, 255, 255), (x[i] * 100 + WIDTH / 2, y[i] * 100 + HEIGHT / 2),
                         (x[i+1] * 100 + WIDTH / 2, y[i+1] * 100 + HEIGHT / 2), 2)

# Specify the number of waves (N) for the blob object
N = 5

# Game loop
running = True
time = 0.0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Create the blob object with time-independent smooth transformation
    x, y = create_blob(N, time)
    

    # Draw the blob object
    draw_blob(x, y)

    pygame.display.flip()
    time += 0.001  # Smaller increment for slower transformation
    clock.tick(20)

# Quit Pygame
pygame.quit()