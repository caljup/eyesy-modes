import pygame
import math
import random
import time
import colorsys

def setup(screen, eyesy):
    global screen_xres, screen_yres, screen_center
    screen_xres = eyesy.xres
    screen_yres = eyesy.yres
    screen_center = (screen_xres // 2, screen_yres // 2)
    
    pygame.display.set_caption("Tri Tri Tri")
    
    global triangle_animator
    triangle_animator = TriangleArmAnimator()

class TriangleArmAnimator:
    def __init__(self):
        self.starting_phase_offsets = [(i * 2 * math.pi) / self.num_arm_parts for i in range(self.num_arm_parts)]
        
        self.phase_positions = self.starting_phase_offsets
        self.max_phase_velocity = 0.1
        self.clockwise_rotation = -1
        
        self.increment_mode_index = 0
        self.increment_modes = ['clockwise','counterclockwise']
        
        self.time_since_last_color_change = 0
        self.color_transition_duration = 3  # seconds
        self.last_time = time.time()

    def increment(self, knob_value, trig):
        if trig:
            self.increment_mode_index = (self.increment_mode_index + 1) % len(self.increment_modes)
            print(f"Switching to increment mode: {self.increment_modes[self.increment_mode_index]}")
        
        if self.phase_positions[0] > 2 * math.pi or self.phase_positions[0] < -2 * math.pi:
            self.phase_reset()
            
        phase_increment = knob_value * self.max_phase_velocity
        
        for i, position in enumerate(self.phase_positions):
            if self.increment_modes[self.increment_mode_index] == "clockwise":
                self.phase_positions[i] = position + phase_increment
            elif self.increment_modes[self.increment_mode_index] == "counterclockwise":
                self.phase_positions[i] = position + phase_increment * self.clockwise_rotation
    
    def phase_reset(self):
        self.phase_positions = [i * 2 * math.pi / self.num_arm_parts for i in range(self.num_arm_parts)]
    
    def draw_sierpinski_triangle(self, screen, x, y, size, color, depth):
        if depth == 0:
            pygame.draw.polygon(screen, color, [(x, y), (x - size / 2, y + size * math.sqrt(3) / 2), (x + size / 2, y + size * math.sqrt(3) / 2)])
        else:
            self.draw_sierpinski_triangle(screen, x, y, size / 2, color, depth - 1)
            self.draw_sierpinski_triangle(screen, x - size / 4, y + size * math.sqrt(3) / 4, size / 2, color, depth - 1)
            self.draw_sierpinski_triangle(screen, x + size / 4, y + size * math.sqrt(3) / 4, size / 2, color, depth - 1)
    
    def update_color_transition(self):
        self.time_since_last_color_change += 0.005 + random.uniform(-0.001, 0.001)  # add a small amount of randomness
        if self.time_since_last_color_change > self.color_transition_duration:
            self.time_since_last_color_change = 0

    def get_triadic_color(self):
        color_palette = [(0.12, 0.71, 0.95), (0.02, 0.83, 0.95), (0.0, 0.0, 1.0), (0.38, 0.56, 0.94), (0.58, 0.67, 0.99)]
        num_colors = len(color_palette)
        color_index = int((self.time_since_last_color_change / self.color_transition_duration) * num_colors) % num_colors
        next_color_index = (color_index + 1) % num_colors
        hue1, saturation1, value1 = color_palette[color_index]
        hue2, saturation2, value2 = color_palette[next_color_index]
        t = (self.time_since_last_color_change / self.color_transition_duration) * num_colors - color_index

        hue = hue1 + (hue2 - hue1) * t
        saturation = saturation1 + (saturation2 - saturation1) * t
        value = value1 + (value2 - value1) * t
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def draw(screen, eyesy):
    pygame.time.Clock().tick(30)
    radius = 300 * eyesy.knob2
    depth = int(eyesy.knob3 * 35)
    
    background_color = eyesy.color_picker_bg(eyesy.knob5)
    color = eyesy.color_picker(eyesy.knob4)
    triangle_animator.update_color_transition()

    radial_scale = 0.5
    radial_change = radius * depth * radial_scale
    sierpinski_size = int(radial_change) # Scale the Sierpinski triangle size with the triangle layer size
    triangle_animator.draw_sierpinski_triangle(screen, screen_center[0], screen_center[1], sierpinski_size, color, depth)
        
    triangle_animator.increment(eyesy.knob1, eyesy.trig)