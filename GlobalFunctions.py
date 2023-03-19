import random
import time
import numpy
import pygame
import copy
from pygame.locals import *

from GlobalFunctions import *

def buildVector(pos1, pos2):
    return [pos1[0] - pos2[0], pos1[1] - pos2[1]]


def vectorLength(vector):
    return numpy.math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def normalizeVector(movment_vector):
    vector_length = vectorLength(movment_vector) # + 0.0001
    if vector_length < 1:
        return pygame.Vector2(0,0)
    return [movment_vector[0] / vector_length, movment_vector[1] / vector_length]
