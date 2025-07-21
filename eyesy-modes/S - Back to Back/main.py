import pygame
import os
import math
import time

def setup(screen, eyesy):
    global xr, yr
    xr = eyesy.xres
    yr = eyesy.yres
    print(xr, yr)
    pygame.display.set_caption("Back to Back")
    
    pass

def draw(screen, eyesy):
    pygame.time.Clock().tick(30)

