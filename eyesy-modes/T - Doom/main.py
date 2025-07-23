import pygame
import sys
import numpy as np
import os
import subprocess
import importlib.util
from typing import Optional
import threading
import time

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path to the cydoomgeneric package
cydoomgeneric_path = os.path.join(current_dir, 'cydoomgeneric')

# Check if cydoomgeneric is already installed
if importlib.util.find_spec('cydoomgeneric') is None:
    # Change to the cydoomgeneric directory
    os.chdir(cydoomgeneric_path)

    # Install the cydoomgeneric package using pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '.'])

import cydoomgeneric as cdg

keymap = {
    pygame.K_LEFT: cdg.Keys.LEFTARROW,
    pygame.K_RIGHT: cdg.Keys.RIGHTARROW,
    pygame.K_UP: cdg.Keys.UPARROW,
    pygame.K_DOWN: cdg.Keys.DOWNARROW,
    pygame.K_COMMA: cdg.Keys.STRAFE_L,
    pygame.K_PERIOD: cdg.Keys.STRAFE_R,
    pygame.K_LCTRL: cdg.Keys.FIRE,
    pygame.K_SPACE: cdg.Keys.USE,
    pygame.K_RSHIFT: cdg.Keys.RSHIFT,
    pygame.K_RETURN: cdg.Keys.ENTER,
    pygame.K_ESCAPE: cdg.Keys.ESCAPE,
}

# Define the static key mapping
key_mapping = {
    'knob1': {
        1.0 : pygame.K_LEFT,
    },
    'knob2': {
        1.0 : pygame.K_UP
    },
    'knob3': {
        1.0 : pygame.K_RIGHT
    },
    'knob4': {
        1.0 : pygame.K_a
    },
    'knob5': {
        1.0 : pygame.K_RETURN
    }
}

knobs = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5, "step": 0.1}

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
        f"Audio Trig: {'On' if eyesy_instance.trig else 'Off'}",
        f"Audio In: {eyesy_instance.audio_in[0]:.2f}",
    ]
    for line in info_lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, y_offset))
        y_offset += 15

class PygameDoom:

    def __init__(self, eyesy) -> None:
        self._resx = eyesy.xres
        self._resy = eyesy.yres
        self.eyesy = eyesy
        self._screen = pygame.display.get_surface()
        self._pixels = np.zeros((self._resy, self._resx, 3), dtype=np.uint8)
        self.prev_knob_values = {1: eyesy.knob1, 2: eyesy.knob2, 3: eyesy.knob3, 4: eyesy.knob4, 5: eyesy.knob5, "step": 0.01}
        self.debounce_time = 0.5  # 100ms debounce time
        self.last_event_time = 0

    def draw_frame(self, pixels: np.ndarray) -> None:
        pixels = np.rot90(pixels)
        pixels = np.flipud(pixels)
        pygame.surfarray.blit_array(self._screen, pixels[:, :, [2, 1, 0]])
        # display_info(self._screen, self.eyesy)
        pygame.display.flip()

    def update_knobs(self, key, knobs):
        """Update knob values based on key presses."""
        for knob_id in range(1, 6):
            if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_i]:
                knobs[knob_id] = min(knobs[knob_id] + knobs["step"], 1.0)
            if key[getattr(pygame, f"K_{knob_id}")] and key[pygame.K_k]:
                knobs[knob_id] = max(knobs[knob_id] - knobs["step"], 0.0)
            setattr(self.eyesy, f"knob{knob_id}", knobs[knob_id])
        return knobs

    def get_key(self) -> Optional[tuple[int, int]]:
        pygame.key.set_repeat(0, 0)
        key = pygame.key.get_pressed()
        kl = []
        for k in key:
            if key[k]:
                kl.append(k)
        updated_knobs = self.update_knobs(key, knobs)

        # Check if any knobs are in a zone that triggers a keyboard input
        for knob_id, values in key_mapping.items():
            knob_val = self.eyesy.__dict__[knob_id]
            if knob_val == 1.0:
                event_type = pygame.KEYDOWN
                event_key = values[knob_id]
                if pygame.time.get_ticks() - self.last_event_time > self.debounce_time:
                    pygame.event.post(pygame.event.Event(event_type, key=event_key))
                    self.last_event_time = pygame.time.get_ticks()
                else:
                    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=event_key))
            # elif self.prev_knob_values[knob_id] == 1.0:
            #     event_type = pygame.KEYUP
            #     event_key = values[1.0]
            #     pygame.event.post(pygame.event.Event(event_type, key=event_key))

        # Process any events that were posted to the queue
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in keymap:
                    return 1, keymap[event.key]
            if event.type == pygame.KEYUP:
                if event.key in keymap:
                    return 0, keymap[event.key]

        events.clear()

        # Allow other game events to be processed
        pygame.time.Clock().tick(60)

        self.prev_knob_values = updated_knobs
        pygame.key.set_mods(0)

        return None

    def set_window_title(self, t: str) -> None:
        pygame.display.set_caption(t)
        
initialized = False
def setup(screen, eyesy):
    global g, initialized
    if not initialized:
        g = PygameDoom(eyesy)
        cdg.init(g._resx, g._resy, g.draw_frame, g.get_key, set_window_title=g.set_window_title)
        
        initialized = True

def draw(screen, eyesy):
    cdg.main()
    