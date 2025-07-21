import pygame
import math

chart_index = 0

def setup(screen, eyesy):
    global chart_index
    chart_index = 0

def draw(screen, eyesy):
    global chart_index
    pygame.time.Clock().tick(30)
    screen.fill((0,0,0)) # clear the screen
    data = eyesy.audio_in # use audio input as data for the charts
    total = sum(abs(i) for i in data) # calculate the total magnitude of the data

    if eyesy.trig:
        global chart_index
        chart_index = (chart_index + 1) % 3

    if chart_index == 0:
        # Draw line chart
        x_scale = eyesy.xres / len(data) # scale x coordinates to fit the screen
        y_scale = eyesy.yres / 32767 # scale y coordinates to fit the screen
        last_x = 0
        last_y = eyesy.yres / 2 # start drawing from the middle of the screen
        for i, value in enumerate(data):
            x = i * x_scale
            y = eyesy.yres / 2 - value * y_scale / 2 # center the chart vertically
            pygame.draw.line(screen, (255,0,0), (last_x, last_y), (x, y), 2)
            last_x = x
            last_y = y
        font = pygame.font.Font(None, 36)
        text = font.render("Line Chart", True, (255,0,0))
        screen.blit(text, (10, 10))

    elif chart_index == 1:
        # Draw bar chart
        bar_width = 20 # width of each bar
        bar_spacing = 10 # spacing between bars
        x_offset = 50 # offset from the left edge of the screen
        y_offset = 50 # offset from the top edge of the screen
        x_scale = (eyesy.xres - 2 * x_offset) / len(data) # scale x coordinates to fit the screen
        y_scale = (eyesy.yres - 2 * y_offset) / 32767 # scale y coordinates to fit the screen

        # Draw x-axis
        pygame.draw.line(screen, (255,255,255), (x_offset, eyesy.yres - y_offset), (eyesy.xres - x_offset, eyesy.yres - y_offset), 2)

        # Draw y-axis
        pygame.draw.line(screen, (255,255,255), (x_offset, y_offset), (x_offset, eyesy.yres - y_offset), 2)

        # Draw bars
        for i, value in enumerate(data):
            x = x_offset + i * (bar_width + bar_spacing)
            y = eyesy.yres - y_offset - abs(value) * y_scale
            pygame.draw.rect(screen, (0,255,0), (x, y, bar_width, eyesy.yres - y_offset - y))

        # Draw x-axis labels
        font = pygame.font.Font(None, 24)
        for i, value in enumerate(data):
            text = font.render(str(i), True, (255,255,255))
            screen.blit(text, (x_offset + i * (bar_width + bar_spacing) - text.get_width() / 2, eyesy.yres - y_offset + 20))

        # Draw y-axis labels
        for i in range(5):
            y = eyesy.yres - y_offset - i * (eyesy.yres - 2 * y_offset) / 4
            text = font.render(str(int(32767 * i / 4)), True, (255,255,255))
            screen.blit(text, (x_offset - 20, y - text.get_height() / 2))

        font = pygame.font.Font(None, 36)
        text = font.render("Bar Chart", True, (0,255,0))
        screen.blit(text, (10, 10))

    elif chart_index == 2:
        # Draw pie chart
        radius = min(eyesy.xres, eyesy.yres) / 2 - 20 # calculate the radius of the pie chart
        center_x = eyesy.xres / 2
        center_y = eyesy.yres / 2
        start_angle = 0
        for i, value in enumerate(data):
            angle = (abs(value) / total) * 2 * math.pi
            end_angle = start_angle + angle
            pygame.draw.polygon(screen, (0,0,255), (
                (center_x, center_y),
                (center_x + radius * math.cos(start_angle), center_y + radius * math.sin(start_angle)),
                (center_x + radius * math.cos(end_angle), center_y + radius * math.sin(end_angle))
            ))
            start_angle = end_angle
        font = pygame.font.Font(None, 36)
        text = font.render("Pie Chart", True, (0,0,255))
        screen.blit(text, (10, 10))