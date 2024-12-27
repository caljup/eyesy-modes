import pygame
import os
import math
import time

def setup(screen, etc):
    global xr, yr
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    pygame.display.set_caption("Back to Back")
    
    pass

def draw(screen, etc):
    pygame.time.Clock().tick(30)

