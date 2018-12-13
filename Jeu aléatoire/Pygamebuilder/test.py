# coding=utf-8
# Ce fichier ne fait que présenter les outils disponible.


import pygame
from pygame import *

from Game import Game
from Objet import Objet
from random import randint
class data:
    def __init__(self):
        self.a = 5
        self.b = 6

class MyGame:

    data = data()


print(MyGame.data.a)
MyGame.data.a = 10
print(MyGame.data.a)
MyGame.data = data()
print(MyGame.data.a)

