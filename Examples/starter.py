import pygame
import os
import sys
import random


def setup():
    global size, screen, clock, font, dt, player_pos

    pygame.init()
    size = height, width = 800, 550
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def information():
    info = pygame.display.Info()
    info_text = (info.hw, info.bytesize, info.video_mem)
    wm_info = {
        "bytesize": info_text[1],
        "file": os.ctermid(),
        "sysname": os.uname()[0],
        "machine": os.uname().machine,
        "Version": sys.api_version,
        "Rando": random.randrange(0,100)
    }

    return wm_info

def display_info(info: dict, coor1: int, coor2: int):
    for x, y in info.items():
            value = font.render( str((x, y)), False, (200, 150, 100) )
            screen.blit(value, (coor1, coor2))
            coor2 += 25

def main():
    setup()

    info = information()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill( "purple" )
        screen.fill( "black", (0,0,200,150) )
        coor1 = 0
        coor2 = 0

        display_info(info, coor1, coor2)
        
        pygame.draw.circle(screen, "red", player_pos, 40)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_pos.y -= 350 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_pos.y += 350 * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos.x -= 350 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos.x += 350 * dt

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == '__main__':
    main()
    pygame.quit()