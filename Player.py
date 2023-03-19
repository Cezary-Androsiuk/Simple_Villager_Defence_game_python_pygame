import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *
from Gas import Gas
from Particle import Particle

class Player:
    mouse = [
        [0, 0],  # current
        [0, 0],  # next
        [0, 0]   # next next
    ]
    gun_fire = False
    particle_array = []
    gas_array = []

    money = 0
    money_const = 1

    ammo = 0

    villagers_count_as_score_const = 1
    score = 0

    def __init__(self):
        pass

    # def movePlayer(self, movement_vector):
    #     n_vector = self.normalizeVector(movement_vector)
    #     self.position[0] += n_vector[0] * self.move_speed
    #     self.position[1] += n_vector[1] * self.move_speed
    #     self.gun = pygame.transform.rotate(self.gun, 10)
    #     pass


    def updateGun(self, mouse_pos):
        self.mouse[2] = self.mouse[1]
        self.mouse[1] = self.mouse[0]
        self.mouse[0] = pygame.Vector2(mouse_pos)
        pass

    def gunStartFire(self):
        self.gun_fire = True

    def gunStopFire(self):
        self.gun_fire = False

    def addParticle(self):
        len = vectorLength(buildVector(self.mouse[0], self.mouse[1]))
        direction = normalizeVector(buildVector(self.mouse[0], self.mouse[1]))
        if self.gun_fire:
            for i in range(0, (int)(len), 10):
                for j in range(0, 3):
                    self.particle_array.append(
                        Particle(
                            [self.mouse[0][0] - direction[0] * i + random.randint(-5, 5),
                             self.mouse[0][1] - direction[1] * i + random.randint(-5, 5)],
                            random.randint(4, 8),
                            random.randint(13, 38)
                        )
                    )
                self.ammo += 1
        else:
            self.score += self.villagers_count_as_score_const

    def updateParticle(self):
        for particle in self.particle_array:
            particle.updateParticle()
            if not particle.visible():
                self.particle_array.remove(particle)
        # print(len(self.particle_array))

    def addGas(self):
        len = vectorLength(buildVector(self.mouse[0], self.mouse[1]))
        direction = normalizeVector(buildVector(self.mouse[0], self.mouse[1]))
        if self.gun_fire:
            for i in range(0, (int)(len), 5):
                self.gas_array.append(
                    Gas(
                        [self.mouse[0][0] - direction[0] * i, self.mouse[0][1] - direction[1] * i],
                        10
                    )
                )

    def updateGas(self):
        for gas in self.gas_array:
            gas.update()
            if not gas.visible():
                self.gas_array.remove(gas)

    def getGas(self):
        return self.gas_array

    def update(self):

        self.addParticle()
        self.updateParticle()

        self.addGas()
        self.updateGas()

        self.money += self.money_const
        pass

    def render(self, screen):
        for particle in self.particle_array:
            particle.renderParticle(screen)
        for gass in self.gas_array:
            gass.render(screen)
        # pygame.draw.line(screen, (180, 180, 180), self.mouse[0], self.mouse[1], 1)
        # pygame.draw.line(screen, (180, 180, 180), self.mouse[1], self.mouse[2], 1)
        pass

