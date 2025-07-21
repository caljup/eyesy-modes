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
        self.animation_mode = 0
        self.num_arm_parts = 8
        self.starting_phase_offsets = [i * 2 * math.pi / self.num_arm_parts for i in range(self.num_arm_parts)]
        
        self.phase_positions = self.starting_phase_offsets
        self.max_phase_velocity = 0.1
        self.counterclockwise_rotation = 1
        self.clockwise_rotation = -1
        self.randomize_arm_directions = [1 if random.random() < 0.5 else -1 for _ in range(self.num_arm_parts)]
        
        self.increment_mode_index = 0
        self.increment_modes = ['clockwise','counterclockwise', 'opposite', 'random']
        
        self.time_since_last_color_change = 0
        self.color_transition_duration = 3  # seconds
        self.last_time = time.time()

    def reset(self):
        self.phase_positions = [i * 2 * math.pi / self.num_arm_parts for i in range(self.num_arm_parts)]

    def increment(self, knob_value, trig):
        if trig:
            self.increment_mode_index = (self.increment_mode_index + 1) % len(self.increment_modes)
            print(f"Switching to increment mode: {self.increment_modes[self.increment_mode_index]}")
            
        if self.phase_positions[0] > 2 * math.pi or self.phase_positions[0] < -2 * math.pi:
            self.reset()
        phase_increment = knob_value * self.max_phase_velocity
        
        for i, position in enumerate(self.phase_positions):
            if self.increment_modes[self.increment_mode_index] == "clockwise":
                self.phase_positions[i] = position + phase_increment
            elif self.increment_modes[self.increment_mode_index] == "counterclockwise":
                self.phase_positions[i] = position + phase_increment * self.clockwise_rotation
            elif self.increment_modes[self.increment_mode_index] == "opposite":
                self.phase_positions[i] = position + phase_increment * self.clockwise_rotation if i % 2 == 0 else position + phase_increment
            elif self.increment_modes[self.increment_mode_index] == "random":
                self.phase_positions[i] = position + phase_increment * self.randomize_arm_directions[i]

    def draw_triangle_layer(self, layer_index, screen, horizontal_offset, vertical_offset, color, background_color, radius, triangle_size):
        radial_scale = 0.5
        radial_change = radius * layer_index * radial_scale
        for i in range(len(self.phase_positions)):
            x_center = int(screen_center[0] + math.cos(self.phase_positions[i]) * radial_change)
            y_center = int(screen_center[1] + math.sin(self.phase_positions[i]) * radial_change)
            color = self.get_triadic_color()
            self.draw_outer_triangle_layer(x_center, y_center, screen, horizontal_offset, vertical_offset, (0,0,0))
            self.draw_inner_triangle_layer(x_center, y_center, screen, horizontal_offset, vertical_offset, color, triangle_size)

    def update_color_transition(self):
        self.time_since_last_color_change += 0.005 + random.uniform(-0.001, 0.001)  # add a small amount of randomness
        if self.time_since_last_color_change > self.color_transition_duration:
            self.time_since_last_color_change = 0

    # def get_triadic_color(self):
    #     color_palette = [(255, 231, 76), (255, 89, 100), (255, 255, 255), (107, 241, 120), (53, 167, 255)]
    #     num_colors = len(color_palette)
    #     color_index = int((self.time_since_last_color_change / self.color_transition_duration) * num_colors) % num_colors
    #     next_color_index = (color_index + 1) % num_colors
    #     rgb1 = color_palette[color_index]
    #     rgb2 = color_palette[next_color_index]
    #     t = (self.time_since_last_color_change / self.color_transition_duration) * num_colors - color_index

    #     r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * t)
    #     g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * t)
    #     b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * t)
    #     return (r, g, b)


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

    def draw_triangle_arms(self, screen, horizontal_offset, vertical_offset, color, background_color, num_layers, radius, triangle_size):
        for layer_index in range(num_layers, 1, -1):
            self.draw_triangle_layer(layer_index, screen, horizontal_offset, vertical_offset, color, background_color, radius, triangle_size)
        radial_scale = 0.5
        radial_change = radius * num_layers * radial_scale
        sierpinski_size = int(radial_change) # Scale the Sierpinski triangle size with the triangle layer size
        self.draw_sierpinski_triangle(screen, screen_center[0], screen_center[1] - 150, sierpinski_size, color, 7)
        
    def draw_outer_triangle_layer(self, x_center, y_center, screen, horizontal_offset, vertical_offset, color):
        p1 = (x_center, y_center - vertical_offset)
        p2 = (x_center - horizontal_offset, y_center + vertical_offset)
        p3 = (x_center + horizontal_offset, y_center + vertical_offset)
        pygame.draw.polygon(screen, color, [p1, p2, p3], 1)

    def draw_inner_triangle_layer(self, x_center, y_center, screen, horizontal_offset, vertical_offset, background_color, triangle_size):
        scale_factor = 1.1
        p1 = (x_center, y_center - vertical_offset * scale_factor)
        p2 = (x_center - horizontal_offset * scale_factor, y_center + vertical_offset * scale_factor)
        p3 = (x_center + horizontal_offset * scale_factor, y_center + vertical_offset * scale_factor)
        pygame.draw.polygon(screen, background_color, [p1, p2, p3], triangle_size)
    
    def draw_sierpinski_triangle(self, screen, x, y, size, color, depth):
        color = (0,0,0)
        if depth == 0:
            pass
        else:
            self.draw_sierpinski_triangle(screen, x, y, size / 2, color, depth - 1)
            self.draw_sierpinski_triangle(screen, x - size / 4, y + size * math.sqrt(3) / 4, size / 2, color, depth - 1)
            self.draw_sierpinski_triangle(screen, x + size / 4, y + size * math.sqrt(3) / 4, size / 2, color, depth - 1)

def draw(screen, eyesy):
    pygame.time.Clock().tick(30)
    triangle_center_x_offset = 200 * eyesy.knob2
    triangle_center_y_offset = 200 * eyesy.knob2
    radius = 300 * eyesy.knob2
    num_layers = int(eyesy.knob3 * 35)
    triangle_size = int(eyesy.knob4 * 10)
    
    background_color = eyesy.color_picker_bg(eyesy.knob5)
    color = eyesy.color_picker(eyesy.knob4)
    triangle_animator.update_color_transition()
    
    triangle_animator.draw_triangle_arms(screen, triangle_center_x_offset, triangle_center_y_offset, color, background_color, num_layers, radius, triangle_size)
    triangle_animator.increment(eyesy.knob1, eyesy.trig)