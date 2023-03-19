import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

class Gas:
    position = [0, 0]
    size = 0
    decrease_ratio = 1
    visible_gas = False
    life_time = 0

    def __init__(self, position, size = 10):
        self.position = position
        self.size = size
        self.life_time = 25

    def update(self):
        self.life_time -= 1

    def render(self, screen):
        if self.visible_gas:
            pygame.draw.circle(screen, (97, 222, 42), self.position, self.size)

    def visible(self):
        if self.life_time > 0:
            return True
        else:
            return False