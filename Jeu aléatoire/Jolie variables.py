
from Pygamebuilder.Game import Game
from Pygamebuilder.Objet import Objet
from Pygamebuilder.Personnage import Personnage
from Pygamebuilder.Arme import Arme
from Pygamebuilder.Projectile import Projectile

import pygame
from pygame import *

from time import time


from jeu import JeuAleatoire


J = JeuAleatoire(100)
Game.COULEUR_FOND_ECRAN = (0, 0, 0)

for i in range(len(J.variables)):
    o = Objet(8 + int(i/10)*15, (i%10)*8 + 4, taille=0)
    o.variable = J.variables[i]


while Game.jouer():
    J.update()

    for objet in Game.objets:
        objet.dessiner_barre(1, 100, objet.variable.valeur+100, 200, (255, 255, 255))


    for touche in J.var_touches:
        touche.valeur = 0

    if Game.bouton_appuye(K_a):
        J.var_touches[0].valeur = 1000
    if Game.bouton_appuye(K_z):
        J.var_touches[0].valeur = -1000
    if Game.bouton_appuye(K_e):
        J.var_touches[1].valeur = 1000
    if Game.bouton_appuye(K_r):
        J.var_touches[1].valeur = -1000
        



























        

    

















