import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

class Enemy:
    position = [0, 0]
    move_speed = 2
    size = 20
    alive = True

    health_enemy_color = (65, 65, 65)
    sick_enemy_color = (65, 160, 65)

    current_color = health_enemy_color

    health = 0
    max_health = 0

    poison_duration = 60
    poison_timer = 0

    def __init__(self, spawn_position, size = 20, health = 80):
        self.position = spawn_position
        self.size = size
        self.alive = True
        self.max_health = health
        self.health = self.max_health


    def poison(self):
        self.poison_timer = self.poison_duration

    def update(self, target_postion):
        if self.poison_timer > 0:
            self.health -= 1

            self.poison_timer -= 1
            self.current_color = self.sick_enemy_color
        else:
            self.current_color = self.health_enemy_color

        if self.health <= 0:
            self.alive = False
            return

        direction = normalizeVector(buildVector(self.position, target_postion))
        self.position[0] -= direction[0] * self.move_speed
        self.position[1] -= direction[1] * self.move_speed

    def renderHealthBar(self, screen):
        hb1_size = pygame.Vector2(40, 5)
        hb1_pos = pygame.Vector2(self.position[0] - hb1_size.x/2, self.position[1] - self.size - 10)
        pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(hb1_pos, hb1_size))
        hb2_size = pygame.Vector2(hb1_size.x * (self.health / self.max_health), hb1_size.y)
        hb2_pos = hb1_pos
        pygame.draw.rect(screen, (255, 65, 65), pygame.Rect(hb2_pos, hb2_size))

    def render(self, screen):
        pygame.draw.circle(screen, self.current_color , self.position, self.size)
        self.renderHealthBar(screen)
