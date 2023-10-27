import pygame

grow = False
pumpkin_growth = 0
alpha = 100
alpha_prev = 0
start_line = 0
end_line = 25
counter = 0

def setup(screen, etc):
    global xr, yr, image, font, base_path, script, script_line, prime_font
    xr = etc.xres
    yr = etc.yres
    base_path = etc.mode_root
    image = pygame.image.load(base_path + 'Images/pumpkin.png').convert()
    font = pygame.font.Font(base_path + 'Fonts/scary-halloween/Scary Halloween Font.ttf', 60)
    prime_font = pygame.font.Font(base_path + 'Fonts/courier-prime/CourierPrime-Regular.ttf', 15)
    with open(base_path + '/Text/halloween_script.txt', 'r') as script:
        script_line = script.readlines()
    pass

def draw(screen, etc):
    pygame.time.Clock().tick(20)
    etc.color_picker_bg(0)
    
    _pumpkin_lighting(screen, etc)
    
    if etc.knob5 >= 0.5:
        _script_display(screen, etc)
    elif etc.knob5 > 0:
        text = font.render('Halloween', True, (235, 97, 35))
        screen.blit(text, (int(xr * etc.knob3), int(yr * etc.knob4)))
    else:
        pass
    
    
def _pumpkin_lighting(screen, etc):
    global alpha, alpha_prev, grow, pumpkin_growth
    pumpkin_image_size = (
        int(image.get_width()/4 + pumpkin_growth),
        int(image.get_height()/4 + pumpkin_growth)
        )
    img = pygame.transform.scale(image, pumpkin_image_size)
    alpha_threshold = 200
    alpha_new = sum(map(abs, etc.audio_in[0:50]))/2500
    alpha = alpha + alpha_new - alpha_prev
    alpha_prev = alpha_new
    img.set_alpha(alpha_threshold) if alpha > alpha_threshold else img.set_alpha(alpha)
    
    if grow:
        pumpkin_growth -= 1
        if pumpkin_growth <= 0: grow = False
    else:
        pumpkin_growth += 1
        if pumpkin_growth >= 500: grow = True
    
    img_dest = (int(xr * etc.knob1), int(yr * etc.knob2))
    
    screen.blit(img, img_dest)
    

def _script_display(screen, etc):
    global start_line, end_line, counter, script_line, prime_font
    if start_line >= len(script_line):
        start_line = 0
        end_line = 20
    elif end_line > len(script_line) - 1:
        start_line = len(script_line) - 1
        end_line = len(script_line)
    
    script_lines = script_line[start_line:end_line]
    for i, l in enumerate(script_lines):
        text = prime_font.render(l.replace('\n', ' '), True, (235, 97, 35))
        screen.blit(text, (int(xr * etc.knob3), yr/10 + i*20))
    
    if counter > 20 * etc.knob4:
        start_line += 1
        end_line += 1
        counter = 0
    else:
        counter += 1