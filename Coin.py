import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

class Coin:
    position = pygame.Vector2(0, 0)
    velocity = 2
    vel_mp = 1.2
    size = 6
    value = 0
    collected = False

    def __init__(self, position, value):
        self.position = pygame.Vector2(position)
        self.value = value
        self.collected = False
        self.velocity = random.randint(1,4)
        self.vel_mp = random.randint(11, 15) / 10

    def ready_to_set_collected(self, target):
        x, y = pygame.display.get_surface().get_size()
        if vectorLength(buildVector(self.position, target)) < self.velocity or \
                (self.position.x < 0  or x < self.position.x) or (self.position.y < 0  or y < self.position.y):
            return True

    def update(self, target):
        if self.ready_to_set_collected(target):
            self.collected = True
        direction = normalizeVector(buildVector(self.position, target))
        self.velocity *= self.vel_mp
        self.position.x -= (direction[0] * self.velocity)
        self.position.y -= (direction[1] * self.velocity)
    def render(self, screen):
        pygame.draw.circle(screen, (255,215,0), self.position, self.size)

    def isCollected(self):
        if self.collected:
            return self.value
        else:
            return 0
