import pygame
from pygame import *

from Personnage import Personnage
from Game import Game
from Texte import TexteEcran

from time import time
from random import randint


class MyGame:
    mon_personnage = Personnage(Game.CENTREX / Game.PIXEL_PAR_METRE,
                                     Game.CENTREY / Game.PIXEL_PAR_METRE,
                                     vitesse=15, vitesse_rotation=180, nom="", angle_vision=randint(0, 360))
    mon_personnage.score = 0
    texte_score = TexteEcran(Game.CENTREX, Game.HAUTEUR_ECRAN - 20, "Nombre de mort : 3  Score max : 3")

    score_max = 0
    temps = 0


def ia_ennemi(self):
    self.avancer_vers(MyGame.mon_personnage)
    self.utiliser_arme_sur(MyGame.mon_personnage)


class Exemple2:
    def __init__(self):
        pass

    def jouer(self):
        while Game.jouer():

            for projectile in list(Game.projectiles):
                for personnage in list(Game.personnages):
                    if projectile.personnage is not personnage:
                        if personnage.collision_avec(projectile):
                            personnage.supprimer()
                            projectile.supprimer()
                            if personnage is MyGame.mon_personnage:
                                self.restart()
                            else:
                                MyGame.mon_personnage.score += 1
                                if MyGame.score_max < MyGame.mon_personnage.score:
                                    MyGame.score_max = MyGame.mon_personnage.score

            if time() - MyGame.temps > 3:
                cible = Personnage(randint(0, int(Game.LARGEUR_ECRAN_METRE)), randint(0, int(Game.HAUTEUR_ECRAN_METRE)),
                                   nom="", couleur=(255, 0, 0), nom_ia=ia_ennemi, vitesse_rotation=50)
                MyGame.temps = time()

            # Controle du personnage.
            if Game.bouton_appuye(K_SPACE):
                MyGame.mon_personnage.utiliser_arme()
            if Game.bouton_appuye(K_z):
                MyGame.mon_personnage.avancer()
            if Game.bouton_appuye(K_s):
                MyGame.mon_personnage.reculer()
            if Game.bouton_appuye(K_q) and Game.bouton_appuye(K_d):
                pass
            elif Game.bouton_appuye(K_q):
                MyGame.mon_personnage.pivoter_gauche()
            elif Game.bouton_appuye(K_d):
                MyGame.mon_personnage.pivoter_droit()

            MyGame.texte_score.texte = "Nombre de mort : {0}  Score max : {1}".format(MyGame.mon_personnage.score, MyGame.score_max)



    def restart(self):
        Game.reinitialiser_jeu()
        MyGame.mon_personnage = Personnage(Game.CENTREX / Game.PIXEL_PAR_METRE,
                                           Game.CENTREY / Game.PIXEL_PAR_METRE,
                                    vitesse=15, vitesse_rotation=180, nom="")
        MyGame.mon_personnage.score = 0
        MyGame.temps = 0


if __name__ == '__main__':
    monJeu = Exemple2()
    monJeu.jouer()
    Game.quit()
