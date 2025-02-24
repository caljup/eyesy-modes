import pygame
import random

class Blob:
    def __init__(self, etc):
        self.x = random.uniform(0, etc.xres)
        self.y = random.uniform(0, etc.yres)
        self.etc = etc
        self.radius = random.uniform(10, 50)
        self.speed = random.uniform(-0.5, 0.5)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

    def update(self):
        self.y += self.speed
        if self.y - self.radius < 0 or self.y + self.radius > self.etc.yres:
            self.speed *= -0.9
        self.x += random.uniform(-0.1, 0.1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

def setup(screen, etc):
    global blobs
    blobs = [Blob(etc) for _ in range(10)]

def draw(screen, etc):
    screen.fill((int(etc.knob5 * 255), int(etc.knob5 * 255), int(etc.knob5 * 255)))
    for blob in blobs:
        blob.update()
        blob.color = (int(etc.knob4 * 255), int(etc.knob4 * 255), int(etc.knob4 * 255))
        blob.radius += etc.knob1 * 0.01
        blob.speed *= 1 + etc.knob3 * 0.01
        blob.draw(screen)
    if etc.knob2 > 0.5:
        blobs.append(Blob(etc))
    elif etc.knob2 < 0.5 and len(blobs) > 1:
        blobs.pop()