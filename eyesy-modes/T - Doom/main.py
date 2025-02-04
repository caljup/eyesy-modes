import pygame
import sys
import importlib.util
from typing import Optional
import numpy as np
import os
current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dir, 'cydoomgeneric'))
import cydoomgeneric as cdg

class PygameDoom:

    def __init__(self, etc, cdg) -> None:
        self._resx = etc.xres
        self._resy = etc.yres

    def draw_frame(self, pixels: np.ndarray) -> None:
        pixels = np.rot90(pixels)
        pixels = np.flipud(pixels)
        pygame.surfarray.blit_array(self._screen, pixels[:, :, [2, 1, 0]])
        pygame.display.flip()

    def get_key(self, etc, cdg) -> Optional[tuple[int, int]]:
            if etc.knob1 >= 0.6:
                return 1, cdg.Keys.RIGHTARROW
            elif etc.knob1 <= 0.4:
                return 1, cdg.Keys.LEFTARROW
            elif etc.knob2 >= 0.6:
                return 1, cdg.Keys.UPARROW
            elif etc.knob2 <= 0.4:
                return 1, cdg.Keys.DOWNARROW
            elif etc.audio_trig == True:
                return 1, cdg.Keys.FIRE
            elif etc.knob3 >= 0.5:
                return 1, cdg.Keys.USE

            return None

    def set_window_title(self, t: str) -> None:
        pygame.display.set_caption(t)


def setup(screen, etc):
    global base_path
    base_path = etc.mode_root

    # doom_wad_path = base_path + '/Games/doom.wad'
    # os.putenv('DOOMWADPATH', doom_wad_path)

    cdg.init(etc.xres, etc.yres, g.draw_frame, g.get_key)

    g = PygameDoom(etc, cdg)
    
    # cdg.init(etc.xres, etc.yres, g.draw_frame, g.get_key, set_window_title=g.set_window_title)

    
    pygame.display.set_caption("Doom")
    pass
        

def draw(screen, etc):
    pass


