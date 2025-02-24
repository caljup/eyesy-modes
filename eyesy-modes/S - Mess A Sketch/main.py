import pygame
import random

def setup(screen, etc):
    global drawing, current_pos, mess
    current_pos = (
        (int(etc.knob1 * etc.xres), int((1 - etc.knob2) * etc.yres)), 
        etc.color_picker(etc.knob4), 
        int(etc.knob3 * 0)
        )
    
    drawing = [current_pos]
    mess = False

def draw(screen, etc):
    global drawing, current_pos, mess
    pygame.time.Clock().tick(60)
    
    screen.fill(etc.color_picker_bg(etc.knob5))
    
    if drawing[-1][0] == current_pos[0]:
        drawing[-1] == current_pos
    elif drawing[-1] != current_pos and int(etc.knob3 * 30) > 0:
        drawing.append(current_pos)

    if mess:
        audio_level = abs(etc.audio_in[0]) / 32767.0
        random_offset = int(audio_level * 50) 
        for i in range(1, len(drawing)):
            pygame.draw.line(screen, drawing[i][1], 
                            (drawing[i-1][0][0] + random.randint(-random_offset, random_offset), 
                                        drawing[i-1][0][1] + random.randint(-random_offset, random_offset)), 
                            (drawing[i][0][0] + random.randint(-random_offset, random_offset), 
                                    drawing[i][0][1] + random.randint(-random_offset, random_offset)), 
                            drawing[i][2])
    else:
        for i in range(1, len(drawing)):
            pygame.draw.line(screen, drawing[i][1], drawing[i-1][0], drawing[i][0], drawing[i][2])
            
    if etc.audio_trig:
        mess = not mess
    
    # clear the drawing
    if etc.audio_trig and all((etc.knob1 == 1, etc.knob2 == 1, etc.knob3 == 1, etc.knob4 == 1, etc.knob5 == 1)):
        drawing = [current_pos]  

    current_pos = (
        (int(etc.knob1 * etc.xres), int((1 -etc.knob2) * etc.yres)), 
        etc.color_picker(etc.knob4), 
        int(etc.knob3 * 30)
        )
    
    pygame.draw.line(screen, etc.color_picker(etc.knob4), (int(etc.knob1 * etc.xres), int((1 -etc.knob2) * etc.yres)), (int(etc.knob1 * etc.xres), int((1 -etc.knob2) * etc.yres)), int(etc.knob3 * 30) + 5)