#!/usr/bin/env python3

import importlib
import argparse
import random
import math
import os
import pygame
import sys
import pyaudio
import numpy as np

# Command line argument parsing
parser = argparse.ArgumentParser(description="Critter and Guitari Eyesy program debug environment")
parser.add_argument('module', type=str, help="Filename of the Pygame program to test")
parser.add_argument('-r', '--record', type=int, help="Record out to image sequence for ffmpeg")
args = parser.parse_args()

# Module setup
module_path = args.module.split('.py')[0]
module_ = module_path.split('/')[0]
module_name = module_path.split('/')[-1]
modes_path = os.path.join(os.path.dirname(__file__), 'eyesy-modes/{}'.format(module_))
sys.path.append(modes_path)
eyesy_mode = importlib.import_module(module_name)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Define colors directly
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Knob values and settings
knobs = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5, "step": 0.01}

class Eyesy:
    def __init__(self):
        for knob_id in range(1, 6):
            setattr(self, f"knob{knob_id}", knobs[knob_id])
        self.audio_trig = False
        self.midi_note_new = False
        self.mode_root = os.path.dirname(eyesy_mode.__file__)
        self.xres, self.yres = 1280, 720
        self.audio_in = [random.randint(-32768, 32767) for _ in range(100)]
        self.bg_color = (0, 0, 0)

    def reset(self):
        self.bg_color = (255, 255, 255)
         
    def color_picker_bg(self, val):
        c = float(val)
        r = (1 - (math.cos(c * 3 * math.pi) * 0.5 + 0.5)) * c
        g = (1 - (math.cos(c * 7 * math.pi) * 0.5 + 0.5)) * c
        b = (1 - (math.cos(c * 11 * math.pi) * 0.5 + 0.5)) * c
        color = (r * 255, g * 255, b * 255)
        self.bg_color = color
        return color
    
# This needs to be simplified. C related to the nobe should gradually increase color options if it's linear across r,g,b. Certain values can cause the crazy effects
    def color_picker(self, val):
        """Determine color based on knob4."""
        c = float(val)
        rando = random.randrange(0, 2)
        color = (rando * 255, rando * 255, rando * 255)

        if c > 0.02:
            color = (random.randrange(0, 255),) * 3
        if c > 0.04:
            color = (50, 50, 50)
        if c > 0.06:
            color = (100, 100, 100)
        if c > 0.08:
            color = (150, 150, 150)
        if c > 0.10:
            color = (175, 175, 175)
        if c > 0.12:
            color = (200, 200, 200)
        if c > 0.14:
            color = (250, 250, 250)
        if c > 0.16:
            r = math.sin(c * 2 * math.pi) * .5 + .5
            g = math.sin(c * 4 * math.pi) * .5 + .5
            b = math.sin(c * 8 * math.pi) * .5 + .5
            color = (r * 255,g * 255,b * 255)
        # full ranoms
        if c > .96 :
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        # primary randoms
        if c > .98 :
            r = random.randrange(0, 2) * 255
            g = random.randrange(0, 2) * 255
            b = random.randrange(0, 2) * 255
            color = (r,g,b)

        return color



def update_knobs(key, knobs):
    """Update knob values based on key presses."""
    for knob_id in range(1, 6):
        if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_UP]:
            knobs[knob_id] = min(knobs[knob_id] + knobs["step"], 1.0)
        if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_DOWN]:
            knobs[knob_id] = max(knobs[knob_id] - knobs["step"], 0.0)
        setattr(eyesy_instance, f"knob{knob_id}", knobs[knob_id])

def display_info(screen, eyesy_instance):
    """Display information on the screen."""
    font = pygame.font.Font(None, 20)
    y_offset = 5
    info_lines = [
        f"Mode Root: {eyesy_instance.mode_root}",
        f"Knob1: {eyesy_instance.knob1:.2f}",
        f"Knob2: {eyesy_instance.knob2:.2f}",
        f"Knob3: {eyesy_instance.knob3:.2f}",
        f"Knob4: {eyesy_instance.knob4:.2f}",
        f"Knob5: {eyesy_instance.knob5:.2f}",
        f"Audio Trig: {'On' if eyesy_instance.audio_trig else 'Off'}",
        f"Audio In: {eyesy_instance.audio_in[0]:.2f}",
        f"Background Color: ({eyesy_instance.bg_color[0]:.2f}, {eyesy_instance.bg_color[1]:.1f}, {eyesy_instance.bg_color[2]:.1f})",
        f"Persist: {clear_screen}"
    ]
    for line in info_lines:
        text = font.render(line, True, WHITE)
        screen.blit(text, (10, y_offset))
        y_offset += 15

eyesy_instance = Eyesy()

# Setup eyesy_mode
eyesy_mode.setup(screen, eyesy_instance)

# Main loop
running = True
clear_screen = True  # Flag to control screen clearing
display_info_flag = False

while running:
    if clear_screen:
        screen.fill(eyesy_instance.bg_color)  # Clear the screen with black

    eyesy_mode.draw(screen, eyesy_instance) 

    key = pygame.key.get_pressed()
    update_knobs(key, knobs)
    eyesy_instance.audio_trig = False

    if key[pygame.K_q]:
        running = False
    if key[pygame.K_SPACE]:
        eyesy_instance.audio_trig = True
    if key[pygame.K_z]:
        eyesy_instance.audio_trig = False
    if key[pygame.K_x]:
        eyesy_instance.audio_in = [random.randint(-32768, 32767) for _ in range(100)]
    if key[pygame.K_c]:
        eyesy_instance.audio_in = [random.randint(-300, 300) for _ in range(100)]
    if key[pygame.K_r]:
        eyesy_instance.reset()  # Reset the Eyesy instance
    if key[pygame.K_t]:
        clear_screen = not clear_screen  # Toggle screen clearing
    if key[pygame.K_i]:
        display_info_flag = not display_info_flag  # Toggle display of information

    if display_info_flag:
        display_info(screen, eyesy_instance) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
