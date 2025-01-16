import pygame
import math
import random

def setup(screen, etc):
    global xr, yr
    xr = etc.xres
    yr = etc.yres
    print(xr, yr)
    
    global screen_center, x, y, points
    screen_center = (xr // 2, yr // 2)
    x = screen_center[0]
    y = screen_center[1]
    points = [(x, y)]
    
    global mr_swchwib_image, lip_images, current_lip
    mr_schwib_filepath = etc.mode_root + '/Images/schwibabyyyy.png'
    lip1_filepath = etc.mode_root + '/Images/lip1.png'
    lip2_filepath = etc.mode_root + '/Images/lip2.png'
    lip3_filepath = etc.mode_root + '/Images/lip3.png'
    lip4_filepath = etc.mode_root + '/Images/lip4.png'
    mr_swchwib_image = pygame.image.load(mr_schwib_filepath)
    lip1 = pygame.image.load(lip1_filepath)
    lip2 = pygame.image.load(lip2_filepath)
    lip3 = pygame.image.load(lip3_filepath)
    lip4 = pygame.image.load(lip4_filepath)
    lip_images = [lip1, lip2, lip3, lip4]
    current_lip = 0
    
    global font, meter_font
    font_size = 20
    font_filepath = etc.mode_root + '/Fonts/SuperMario256.ttf'
    font = pygame.font.Font(font_filepath, font_size)
    meter_font = pygame.font.Font(font_filepath, 50)
    
    global spiral_angle_offset, iter_text_x, iter_text_y, text_block_positions
    spiral_angle_offset = 0
    iter_text_x = 0
    iter_text_y = 0
    
    global current_note
    current_note = etc.audio_in[0]
    
    pygame.display.set_caption("Mr. Schwibabyyyy")
    pass
    

def draw(screen, etc):
    pygame.time.Clock().tick(30)
    bg_color = etc.color_picker_bg(etc.knob5)
    color = etc.color_picker(etc.knob4)
    
    mr_schwib_img = load_mr_schwib(screen)
    
    text_display(screen, etc, color, mr_schwib_img, xr, yr)
    draw_hair(screen, color, mr_swchwib_image, etc)
    execute_mouth_mode(screen, color, etc)
    
def load_mr_schwib(screen):
    image_size_x=int(mr_swchwib_image.get_width() * 0.4) if mr_swchwib_image.get_width() > xr else mr_swchwib_image.get_width()
    image_size_y=int(yr) if mr_swchwib_image.get_height() > yr else mr_swchwib_image.get_height()
    image_res = (int(image_size_x), int(image_size_y))
    
    scwib_img = pygame.transform.scale(mr_swchwib_image, image_res)
    screen.blit(scwib_img, (xr // 4.5, 50))
    return scwib_img
    

def execute_mouth_mode(screen, color, etc):
    global points, spiral_angle_offset, x, y
    
    if etc.knob3 < 0.33:
        draw_lip(screen, etc)
    elif etc.knob3 >= 0.33 and etc.knob3 < 0.66:
        spiral_angle_offset += 0.1 * etc.knob2
        if spiral_angle_offset > 2 * math.pi:
            spiral_angle_offset = 0
        base_num_points = 1750
        if etc.knob2 > 0:
            num_points = int(base_num_points * etc.knob2 + 1)
            draw_spiral_line(screen, x, y, 1, num_points, color, spiral_angle_offset)
        else:
            pass
    else:
        if etc.audio_trig == False:
            x, y, points = grow_mouth(x, y, points, etc)
        else:
            decrease_mouth(points)
        draw_mouth(screen, points, color, etc)
        

def grow_mouth(x, y, points, etc):
    dx = random.uniform(-100, 100)
    dy = random.uniform(-100, 100)
    x += dx * etc.knob2
    y += dy * etc.knob2
    
    horizontal_boundary_offset, vertical_boundary_offset = int(1000 * etc.knob2), int(650 * etc.knob2)
    
    horizontal_boundary = (screen_center[0] - horizontal_boundary_offset, screen_center[0] + horizontal_boundary_offset)
    vertical_boundary = (screen_center[1] - vertical_boundary_offset, screen_center[1] + vertical_boundary_offset)
    if x < horizontal_boundary[0] or x > horizontal_boundary[1] or y < vertical_boundary[0] or y > vertical_boundary[1]:
        x, y = screen_center[0], screen_center[1]
        
    if len(points) > 500:
        points.pop(0)
        points.append((x, y))
    else:
        points.append((x, y))
    
    return x, y, points
    
def decrease_mouth(points):
    if len(points) > 1:
        points.pop()
        points.pop(0)
    return points
        
def draw_mouth(screen, points, color, etc):
    for i in range(1, len(points)):
        pygame.draw.line(screen, color, points[i-1], points[i], 4)

def draw_spiral_line(screen,x, y, radius, num_points, color, spiral_angle_offset):
    spiral_points = []
    for i in range(num_points):
        spiral_angle = -i * 0.1 + spiral_angle_offset
        r = radius + i * 0.5
        px = screen_center[0] + r * math.cos(spiral_angle)
        py = screen_center[1] + r * math.sin(spiral_angle)
        spiral_points.append((px, py))
    pygame.draw.lines(screen, color, False, spiral_points, 8)

def draw_lip(screen, etc):
    global lip_images, current_lip, current_note
    
    lip_image = lip_images[current_lip] 
    lip_image_size_x=int(lip_image.get_width() * etc.knob2)
    lip_image_size_y=int(lip_image.get_height() * etc.knob2)
    image_res = (int(lip_image_size_x), int(lip_image_size_y))
    
    img = pygame.transform.scale(lip_image, image_res)
    img_center_x = img.get_width() // 2
    img_center_y = img.get_height() // 2
    
    if etc.knob1 > 0.9:
        offset_x = (screen_center[0] - img_center_x + (etc.audio_in[0] // 1000))
        offset_y = (screen_center[1] - img_center_y + (etc.audio_in[0] // 1000))
        screen.blit(img, (offset_x, offset_y))
    else:
        offset_x = (screen_center[0] - img_center_x)
        offset_y = (screen_center[1] - img_center_y)
        screen.blit(img, (offset_x, offset_y))
        
    if current_note != etc.audio_in[0] :
        current_lip = (current_lip + 1) % len(lip_images)
        current_note = etc.audio_in[0]

def text_display(screen, etc, color, img, xr, yr):
    global iter_text_x, iter_text_y, text_block_positions
    
    text2 = font.render('CAN YOU HEAR ME MR. SCHWIBABYYYY?', True, color)
    SPACING = 5
    
    if etc.knob1 == 1:
        text_position_x = 0
        text_position_y = 0
        while text_position_y < yr:
            screen.blit(text2, (text_position_x, text_position_y))
            text_position_x += text2.get_width() + SPACING
            if text_position_x > xr:
                text_position_x = 0
                text_position_y += text2.get_height() + SPACING
    elif etc.knob1 < 1 and etc.knob1 >= 0.65:
        text_down = iter_text_y
        if iter_text_y > yr + (text2.get_height() + SPACING) * 10:
            iter_text_x += text2.get_width() + SPACING
            iter_text_y = 0 - (text2.get_height() + SPACING) * 10
        
        text_block_positions = []
        
        for text_position in range(0,13):
            text_block_positions.append((iter_text_x, text_down))
            text_down += text2.get_height() + SPACING
            
        for text in text_block_positions:
            screen.blit(text2, (text[0], text[1]))
            
        iter_text_y += 5
            
        if iter_text_x > xr:
            iter_text_x = 0
            iter_text_y = 0 - (text2.get_height() + SPACING) * 10
    elif etc.knob1 < 0.65 and etc.knob1 >= 0.36:
        if etc.audio_in[0] % 2 == 0:
            screen.blit(text2, (xr * 0.01, yr // 5))
        else:
            screen.blit(text2, (xr * 0.67, yr // 5))
    
    text = meter_font.render('DELIRIUM: {}%'.format(int(etc.knob1 * 100)), True, (0,0,0))
    screen.blit(text, (xr - 430, yr - 50))
  
def draw_hair(screen, color, img, etc):
    image_rect = img.get_rect(center=(screen_center[0] // 2, screen_center[1] // 2))
    
    num_lines = 10
    angle_step = math.pi / num_lines
    radius = 150
    line_spacing = xr/num_lines
    center_x, center_y = xr // 2.25 + 25, image_rect.centery
    line_positions = []
    
    for i in range(1, num_lines + 1):
        angle = i * angle_step
        x1 = center_x + radius * math.cos(angle)
        y1 = center_y - 100 * math.sin(angle)
        x2 = center_x + (radius + line_spacing * etc.knob1 * i) * math.cos(angle + math.pi / 6 + etc.audio_in[0] / 100)
        y2 = 0
        line_positions.append(((x1, y1), (x2, y2)))
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)
    
    
