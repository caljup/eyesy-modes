import pygame
import os
import math
import time

def setup(screen, eyesy):
    global xr, yr, img, font, font_size
    xr = eyesy.xres
    yr = eyesy.yres
    print(xr, yr)
    
    filepath = eyesy.mode_root + '/Images/billy-bat.png'
    img = pygame.image.load(filepath)
    font_size = 50
    font_filepath = eyesy.mode_root + '/Fonts/Square Chunks.ttf'
    font = pygame.font.Font(font_filepath, font_size)
    pass

def draw(screen, eyesy):
    pygame.time.Clock().tick(30)
    
    bg_color = eyesy.color_picker_bg(eyesy.knob5)
    color = eyesy.color_picker(eyesy.knob4)
    # text_color = (color[0],int(127 + 127 * math.sin(25 * .0001 + time.time())),color[2])
    
    text = font.render('97.1  :  Beat Bat', True, color)
    text2 = font.render('97.1  :  Beat Bat', True, bg_color)
    offset = (1 + font_size//15)
    screen.blit(text, (50, 50))
    screen.blit(text2, (50 + offset, 50 - offset))
    screen.blit(text, (50 + offset * 2, 50 - offset * 2))
    
    point = int(eyesy.knob3 * 100)
    audio_flux = abs(int(eyesy.audio_in[0] / 100))
    audio_flux2 = abs(int(eyesy.audio_in[0] / 100))
    
    for i in range(0, 13):
        poly_points1 = []
        poly_points2 = []
        
        for pp in range(0, 5):
            poly_points1.append(
                ((xr - point * pp) + audio_flux - (i * 100) , (yr - point * pp) + (i * 15) + audio_flux2 )
                )
            poly_points2.append(
                ((xr - point * pp) + audio_flux - (i * 100) , (30 + point * pp) + (i * 15) + audio_flux2 )
                )
        
        pygame.draw.polygon(screen, color, poly_points1, 100 )
        pygame.draw.polygon(screen, color, poly_points2, 75 )
    
    if eyesy.knob1 != 0.0:
        image_size_x=int(img.get_width() * eyesy.knob1)
        image_size_y=int(img.get_height() * eyesy.knob1)
        image_res = (int(image_size_x), int(image_size_y))
        image = pygame.transform.scale(img, image_res)
        image = pygame.transform.rotate(image, eyesy.knob2 * 100)
        screen.blit(image, (xr * .6 ,yr/2.75))
        