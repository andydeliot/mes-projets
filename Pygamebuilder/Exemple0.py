# coding=utf-8
# Ce fichier ne fait que présenter les outils disponible.


import pygame
from pygame import *

from Game import Game
from Objet import Objet
from Personnage import Personnage
from Texte import TexteObjet, TexteEcran
from Bouton import BoutonObjet, BoutonEcran


def ia_personnage(self):
    if self.actif:
        self.pivoter_gauche()
        self.avancer()


class Exemple0:

    def __init__(self):
        un_objet = Objet()
        un_personnage = Personnage(nom_ia=ia_personnage)
        un_personnage.actif = False
        un_texte_objet = TexteObjet()
        un_texte_ecran = TexteEcran()
        un_bouton_objet = BoutonObjet()
        un_bouton_ecran = BoutonEcran()

        while Game.jouer():

            if Game.clic_gauche():
                pos = Game.position_souris()

            if Game.mouvement_souris() and Game.etat_clic_gauche:
                pos2 = Game.position_souris()
                Game.Vision.visionx -= (pos[0] - pos2[0]) / Game.Vision.zoom
                Game.Vision.visiony -= (pos[1] - pos2[1]) / Game.Vision.zoom
                pos = list(pos2)

            if Game.molette_haut():
                Game.Vision.zoom *= 1.1
            if Game.molette_bas():
                Game.Vision.zoom *= 0.9

            if un_bouton_objet.clique():
                un_objet.x += 5
                un_bouton_objet.x += 5

            if un_bouton_ecran.clique():
                un_personnage.actif = not un_personnage.actif
                # un_personnage.avancer()


if __name__ == '__main__':
    Exemple0()
    Game.quit()

