import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

class Particle:
    position = [0, 0]
    size = 0
    decrease_ratio = 0.0
    left_time = 0
    def __init__(self, position, size = 1, life_time = 120):
        self.position = position
        if position[0] < 0:
            self.position[0] = 0

        if position[1] < 0:
            self.position[1] = 0
        self.size = size
        self.decrease_ratio = size / life_time
        self.left_time = life_time

    def updateParticle(self):
        self.left_time -= 1
        self.size -= self.decrease_ratio

    def renderParticle(self, screen):
        pygame.draw.rect(
            screen,
            (
                97 + random.randint(-10, 10),
                222 + random.randint(-10, 10),
                42 + random.randint(-10, 10)
            ),
            pygame.Rect(self.position[0], self.position[1], self.size, self.size))

    def visible(self):
        if self.size > 0:
            return True
        else:
            return False

