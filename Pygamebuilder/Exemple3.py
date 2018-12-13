import pygame
from pygame import *

from Personnage import Personnage
from Projectile import Projectile
from Game import Game
from Texte import TexteEcran

from time import time
from random import randint

coef_vitesse = 1.

Projectile.vitesse = Projectile.vitesse * coef_vitesse
Projectile.temps_de_vie_max = Projectile.temps_de_vie_max / coef_vitesse

def creer_cible(posx, posy, angle_vision):
    cible = Personnage(posx, posy, nom="", couleur=(255, 0, 0), nom_ia=ia_ennemi, vitesse=25*coef_vitesse, vitesse_rotation=360*coef_vitesse, angle_vision=angle_vision)


class MyGame:
    un_personnage = Personnage(Game.CENTREX / Game.PIXEL_PAR_METRE,
                      Game.CENTREY / Game.PIXEL_PAR_METRE,
                      vitesse=50*coef_vitesse, vitesse_rotation=10000, nom="", angle_vision=randint(0, 360))
    un_personnage.score = 0
    un_personnage.arme_primaire.frequence_utilisation = 0
    texte_score = TexteEcran(Game.CENTREX, Game.HAUTEUR_ECRAN - 20, "Nombre de mort : 3  Score max : 3")

    score_max = 0
    temps = 0

    Projectile.taille = 0.5

    @staticmethod
    def restart():
        global mon_personnage
        Game.reinitialiser_jeu()
        mon_personnage = creer_perso()


def ia_ennemi(self):
    self.avancer_vers(mon_personnage)
    self.utiliser_arme_sur(mon_personnage)


def creer_perso():
    un_personnage = Personnage(Game.CENTREX / Game.PIXEL_PAR_METRE,
                      Game.CENTREY / Game.PIXEL_PAR_METRE,
                      vitesse=50*coef_vitesse, vitesse_rotation=10000, nom="", angle_vision=randint(0, 360))
    un_personnage.score = 0
    un_personnage.arme_primaire.frequence_utilisation = 0
    return un_personnage


class Exemple3:
    def __init__(self):
        pass

    def jouer(self):
        MyGame.restart()

        texte_debut = TexteEcran(texte="Clic droit pour commencer")

        score_max = 0
        dernier_score = 0

        level = -1

        spawning = True
        temps = 0
        start = False
        while Game.jouer(): 
            # Orientation personnage.
            mon_personnage.orienter_vers(mon_personnage.position_logique(Game.position_souris()))

            if start:
                if level == -1:
                    if time() - temps > 1:
                        spawning = True
                    if spawning:
                        while True:
                            posx = randint(0, int(Game.LARGEUR_ECRAN_METRE))
                            posy = randint(0, int(Game.HAUTEUR_ECRAN_METRE))
                            if mon_personnage.distance_avec((posx, posy)) > 75:
                                break
                        cible = Personnage(posx, posy, nom="", couleur=(255, 0, 0), nom_ia=ia_ennemi,
                                           vitesse=25*coef_vitesse, vitesse_rotation=360*coef_vitesse, angle_vision=randint(0, 360))
                        cible.arme_primaire.frequence_utilisation = cible.arme_primaire.frequence_utilisation / coef_vitesse
                        spawning = False
                        temps = time()

                if level == 1:
                    if spawning:
                        creer_cible(Game.LARGEUR_ECRAN_METRE/2 - 40, Game.HAUTEUR_ECRAN_METRE/2, angle_vision=0)
                        creer_cible(Game.LARGEUR_ECRAN_METRE/2 + 40, Game.HAUTEUR_ECRAN_METRE/2, angle_vision=180)
                        spawning = not spawning


                # Changement de niveau.
                if Game.bouton_appuye(K_u):
                    level = 1
                    MyGame.restart()
                    spawning = True
                if Game.bouton_appuye(K_i):
                    level = -1
                    MyGame.restart()
                
                # Tir.
                if Game.clic_gauche():
                    Projectile.couleur = (50, 50, 50)
                    mon_personnage.utiliser_arme()
                    Projectile.couleur = (125, 125, 125)

                # Controle du personnage.
                if Game.bouton_appuye(K_z):
                    mon_personnage.y -= mon_personnage.vitesse * Game.PERIODE
                if Game.bouton_appuye(K_s):
                    mon_personnage.y += mon_personnage.vitesse * Game.PERIODE
                if Game.bouton_appuye(K_q) and Game.bouton_appuye(K_d):
                    pass
                elif Game.bouton_appuye(K_q):
                    mon_personnage.x -= mon_personnage.vitesse * Game.PERIODE
                elif Game.bouton_appuye(K_d):
                    mon_personnage.x += mon_personnage.vitesse * Game.PERIODE

                # Mur.
                if mon_personnage.x < mon_personnage.taille:
                    mon_personnage.x = mon_personnage.taille
                elif mon_personnage.x > Game.LARGEUR_ECRAN_METRE - mon_personnage.taille:
                    mon_personnage.x = Game.LARGEUR_ECRAN_METRE - mon_personnage.taille

                if mon_personnage.y < mon_personnage.taille:
                    mon_personnage.y = mon_personnage.taille
                elif mon_personnage.y > Game.HAUTEUR_ECRAN_METRE - mon_personnage.taille:
                    mon_personnage.y = Game.HAUTEUR_ECRAN_METRE - mon_personnage.taille


                # Collision avec les projectiles.
                for projectile in list(Game.projectiles):
                    for personnage in list(Game.personnages):
                        if projectile.personnage is not personnage:
                            if personnage.collision_avec(projectile):
                                personnage.supprimer()
                                try:
                                    projectile.supprimer()
                                except:
                                    pass
                                if personnage is mon_personnage:
                                    dernier_score = mon_personnage.score
                                    MyGame.restart()
                                else:
                                    mon_personnage.score += 1
                                    if score_max < mon_personnage.score:
                                        score_max = mon_personnage.score

            else:
                texte_debut.afficher()
                if Game.clic_droit():
                    start = True
                    texte_debut.cacher()

            MyGame.texte_score.texte = "Nombre de mort : {0}  Score max : {1}  Dernier score : {2}".format(mon_personnage.score,
                                                                                                    score_max, dernier_score)


if __name__ == "__main__":
    Exemple3().jouer()
