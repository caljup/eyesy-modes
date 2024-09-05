import pygame
import os

def setup(screen, etc):
    global xr, yr, image, text_font_path
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    
    base_path = etc.mode_root
    image = pygame.image(base_path + '/Images/car.png')
    text_font_path = pygame.font.Font(base_path + '/Fonts/panamera/Panamera-Regular.otf', size = 50)
    pass

def draw(screen, etc):
    
    bg_color = etc.color_picker_bg(etc.knob5)
    # color = etc.color_picker(etc.knob4)
    
    #Knob 1 - Adjust size of images
    car_image_size = (int(image.get_width() * etc.knob1), int(image.get_height() * etc.knob1))
    image = pygame.transform.scale(image, car_image_size)
    
    #adjust knob 3 to set the trigger pattern. Set in a differnt function? Pass if knob value is the same as last frame
    #Pattern 0: Value of Knob is 0. Causes all pictures to show
    #Pattern 1: Rotate between four images on audio trigger
    #Pattern 2: Reverse Image rotation
    #Pattern 3: Randomize image shown
    #Pattern 4: Show random image somewhere on screen
    if etc.knob3 == 0:
        screen.blit(image)
    elif etc.knob4 < .25:
        if etc.audio_trig == True:
            dest =(int(xr * etc.knob1), int(yr * etc.knob1))
            screen.blit(image, dest)
    elif etc.knob4 < .5:
        screen.blit(image)
    elif etc.knob4 < .75:
        screen.blit(image)
    else:
        screen.blit(image)
    
    
    
    #On audio trigger, show an image
    etc.audio_trig = True
    
    
    pass