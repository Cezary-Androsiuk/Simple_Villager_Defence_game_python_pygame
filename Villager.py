import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

class Villager:
    spawn_position = [0, 0]
    position = [0, 0]
    move_speed = 2.1
    size = 20
    alive = True
    see_range = 100

    # prev1_enemy_pos = [0, 0]

    health = 0
    max_health = 0

    def __init__(self, spawn_position, see_range = 100, size = 20, health = 1000):
        self.spawn_position = copy.copy(spawn_position)
        self.position = spawn_position
        # self.prev1_enemy_pos = self.position
        self.size = size
        self.see_range = see_range
        self.alive = True
        self.max_health = health
        self.health = self.max_health

    def dealDamage(self, damage):
        self.health -= damage

    def villagerNotOnDisplay(self):
        x, y = pygame.display.get_surface().get_size()
        if self.position[0] < 0 or self.position[0] > x or self.position[1] < 0 or self.position[1] > y:
            return True
        else:
            return False

    def update(self, escape_position):
        if self.health <= 0 or self.villagerNotOnDisplay():
            self.alive = False
            return

        if vectorLength(buildVector(self.position, escape_position)) < self.see_range:
            direction = normalizeVector(buildVector(self.position, [
                escape_position[0], # + self.prev1_enemy_pos[0], #+ self.prev2_enemy_pos[0],
                escape_position[1] # + self.prev1_enemy_pos[1] #+ self.prev2_enemy_pos[1]
            ]))
            self.position[0] += direction[0] * self.move_speed
            self.position[1] += direction[1] * self.move_speed
            # self.prev1_enemy_pos = escape_position
        else:
            direction = normalizeVector(buildVector(self.position, self.spawn_position))
            # print(self.spawn_position, self.position)
            self.position[0] -= direction[0] * self.move_speed
            self.position[1] -= direction[1] * self.move_speed
        # self.prev2_enemy_pos = self.prev1_enemy_pos



    def renderHealthBar(self, screen):
        hb1_size = pygame.Vector2(40, 5)
        hb1_pos = pygame.Vector2(self.position[0] - hb1_size.x/2, self.position[1] - self.size - 10)
        pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(hb1_pos, hb1_size))
        hb2_size = pygame.Vector2(hb1_size.x * (self.health / self.max_health), hb1_size.y)
        hb2_pos = hb1_pos
        pygame.draw.rect(screen, (255, 65, 65), pygame.Rect(hb2_pos, hb2_size))

    def render(self, screen):
        pygame.draw.circle(screen, (65, 65, 255), self.position, self.size)
        self.renderHealthBar(screen)