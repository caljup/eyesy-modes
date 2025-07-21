import pygame
import random

class Blob:
    def __init__(self, eyesy):
        self.x = random.uniform(0, eyesy.xres)
        self.y = random.uniform(0, eyesy.yres)
        self.eyesy = eyesy
        self.radius = random.uniform(10, 50)
        self.speed = random.uniform(-0.5, 0.5)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

    def update(self):
        self.y += self.speed
        if self.y - self.radius < 0 or self.y + self.radius > self.eyesy.yres:
            self.speed *= -0.9
        self.x += random.uniform(-0.1, 0.1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

def setup(screen, eyesy):
    global blobs
    blobs = [Blob(eyesy) for _ in range(10)]

def draw(screen, eyesy):
    screen.fill((int(eyesy.knob5 * 255), int(eyesy.knob5 * 255), int(eyesy.knob5 * 255)))
    for blob in blobs:
        blob.update()
        blob.color = (int(eyesy.knob4 * 255), int(eyesy.knob4 * 255), int(eyesy.knob4 * 255))
        blob.radius += eyesy.knob1 * 0.01
        blob.speed *= 1 + eyesy.knob3 * 0.01
        blob.draw(screen)
    if eyesy.knob2 > 0.5:
        blobs.append(Blob(eyesy))
    elif eyesy.knob2 < 0.5 and len(blobs) > 1:
        blobs.pop()