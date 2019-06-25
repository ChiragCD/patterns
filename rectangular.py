import pygame, random

"""
Movers move in compass directions and randomly create nodes and reproduce there, moving off
in various compass directions. Trace their paths as they go.
"""

class mover(object):

    def __init__(self):

        pass

class node(object):

    def __init__(self, position):

        self.x = position[0]
        self.y = position[1]
