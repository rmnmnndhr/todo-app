import pygame, random
from settings import *

class Particle:
    def __init__(self):
        self.pos = (random.randrange(0, WIDTH), random.randrange(-200, -10))
        self.vertices = [(0,0),(4,15),(0,20),(-4,15)]

        self.coordinates = [(self.vertices[0][0] + self.pos[0], self.vertices[0][1] + self.pos[1]),(self.vertices[1][0] + self.pos[0], self.vertices[1][1] + self.pos[1]),
                            (self.vertices[2][0] + self.pos[0], self.vertices[2][1] + self.pos[1]),(self.vertices[3][0] + self.pos[0], self.vertices[3][1] + self.pos[1])]

        self.speed = random.randrange(200,500)

    def draw(self, screen):
        pygame.draw.polygon(screen, RAIN, self.coordinates)


    def update(self, dt):
        self.pos = (self.pos[0], self.pos[1] + self.speed * dt)
        self.coordinates = [(self.vertices[0][0] + self.pos[0], self.vertices[0][1] + self.pos[1]),(self.vertices[1][0] + self.pos[0], self.vertices[1][1] + self.pos[1]),
                            (self.vertices[2][0] + self.pos[0], self.vertices[2][1] + self.pos[1]),(self.vertices[3][0] + self.pos[0], self.vertices[3][1] + self.pos[1])]
