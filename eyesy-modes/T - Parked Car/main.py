import pygame
import random

def setup(screen, eyesy):
    global xr, yr, counter, quarters, image, font
    xr = eyesy.xres
    yr = eyesy.yres
    print(xr, yr)
    counter = 0
    
    quarters = [(xr*0.1, 0), (xr*0.6, 0), (xr*0.1, yr*0.5), (xr*0.6, yr*0.5)]
    
    base_path = eyesy.mode_root
    image = pygame.image.load(base_path + '/Images/car.png')
    font = pygame.font.Font(base_path + '/Fonts/panamera/Panamera-Bold.otf', 100)
    pass

def draw(screen, eyesy):
    global counter
    pygame.time.Clock().tick(15)
    
    bg_color = eyesy.color_picker_bg(eyesy.knob5)
    car_image_size = (int(image.get_width() * eyesy.knob1), int(image.get_height() * eyesy.knob1))
    img = pygame.transform.scale(image, car_image_size)
    
    if eyesy.trig == True:
        #Single Top Left Corner Display
        if eyesy.knob4 == 0:
            screen.blit(img, (0,0))
        #Multiple Image At Once Display
        elif eyesy.knob4 < .25:
            count = 0
            while count < 1:
                dest_top = (xr * count, yr * 0.5)
                dest_bottom = (xr * count, 0)
                screen.blit(img, dest_top)
                screen.blit(img, dest_bottom)
                count += 0.25
        #Display Image Randomly
        elif eyesy.knob4 < .5:
            random_dest = ( xr * random.choice([x/4.0 for x in range(0,4)]), yr * random.choice([x/4.0 for x in range(0,4)]))
            screen.blit(img, random_dest)
        #Adjust Image Position Display
        elif eyesy.knob4 < .75:
            dest = (int(xr * eyesy.knob2), int(yr * eyesy.knob3))
            screen.blit(img, dest)
        #Quarter Display
        elif eyesy.knob4 < 1.0:
            if counter > 3:
                counter = 0
            screen.blit(img, quarters[counter])
            counter += 1
        else:
            pass
    #Gotta Park Da Car
    if eyesy.knob4 == 1.0:
        text = font.render('Hold On, Gotta Park.', True, (0, 255, 0))
        screen.blit(text, (xr*.1, yr/2.5))