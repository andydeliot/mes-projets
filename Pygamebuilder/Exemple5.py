import pygame
from pygame import *

from Personnage import Personnage
from Projectile import Projectile
from Arme import Arme
from Objet import Objet
from Game import Game
from Texte import TexteEcran

from time import time
from random import randint, choice


heros = Personnage(vitesse=20)
viseur = Objet(taille=0.1)


def ia_zombie(self):
    self.avancer_vers(heros)

def ia_zombie2(self):
    if self.distance_avec(heros) > 30:
        self.orienter_vers(heros)
        self.deplacement_gauche()
    elif self.distance_avec(heros) > 60:
        self.orienter_vers(heros)
        self.deplacement_droite()
    else:
        self.avancer_vers(heros)


Projectile.vitesse = 200
Projectile.temps_de_vie_max = 0.5

heros.arme_primaire.frequence_utilisation = 0.25
heros.arme_primaire.munitions_max = 10
heros.arme_primaire.munitions = heros.arme_primaire.munitions_max / 2

Game.munitions = []
class Munition(Objet):
    def __init__(self):
        Objet.__init__(self, randint(0, int(Game.LARGEUR_ECRAN_METRE)), randint(0, int(Game.HAUTEUR_ECRAN_METRE)), taille=0.5, couleur=(150, 150, 150))
        Game.munitions.append(self)

spawn = time()
spawn_munition = time()
while Game.jouer():
    
    # Fond écran.
    if heros.arme_primaire.temps_derniere_utilisation < 0.05:
        Game.COULEUR_FOND_ECRAN = (20, 20, 0)
    else:
        Game.COULEUR_FOND_ECRAN = (0, 0, 0)

    # Monstre.
    if time() - spawn >= 2:
        p = Personnage(x=randint(0, Game.LARGEUR_ECRAN_METRE), y=-2,
                   vitesse=randint(10, 300)/10,
                   taille=randint(10, 50)/10,
                   nom="", nom_equipe="Zombie",
                   nom_ia=choice([ia_zombie, ia_zombie2]), couleur=(255, 0, 0))
        p.pv_max = randint(50, 300)
        p.pv = p.pv_max
        spawn = time()
    for monstre in list(Game.personnages):
        if monstre is not heros:
            if monstre.collision_avec(heros):
                heros.pv -= 1

    # Munition.
    if time() - spawn_munition >= 3:
        Munition()
        spawn_munition = time()

    for munition in list(Game.munitions):
        if heros.collision_avec(munition):
            heros.arme_primaire.munitions += 5
            munition.supprimer()
            Game.munitions.remove(munition)
    # Déplacement.
    viseur.x, viseur.y = Game.position_souris()[0]/Game.PIXEL_PAR_METRE, Game.position_souris()[1]/Game.PIXEL_PAR_METRE
    heros.orienter_vers(viseur)
    orientation = heros.angle_vision
    if Game.bouton_appuye(K_z):
        heros.angle_vision = -90
        heros.avancer()
        heros.cycle_deplacement = True
    if Game.bouton_appuye(K_s):
        heros.angle_vision = 90
        heros.avancer()
        heros.cycle_deplacement = True
    if Game.bouton_appuye(K_q):
        heros.angle_vision = 180
        heros.avancer()
        heros.cycle_deplacement = True
    if Game.bouton_appuye(K_d):
        heros.angle_vision = 0
        heros.avancer()
        heros.cycle_deplacement = True
    heros.angle_vision = orientation

    # Tir.
    if Game.clic_gauche():
        heros.utiliser_arme()
        temps_tir = 0

    for projectile in list(Game.projectiles):
        for personnage in list(Game.personnages):
            if personnage is not heros:
                if projectile.collision_avec(personnage):
                    personnage.pv -= 55
                    projectile.supprimer()
                    break

    # Mur.
    if heros.x < heros.taille:
        heros.x = heros.taille
    elif heros.x > Game.LARGEUR_ECRAN_METRE - heros.taille:
        heros.x = Game.LARGEUR_ECRAN_METRE - heros.taille

    if heros.y < heros.taille:
        heros.y = heros.taille
    elif heros.y > Game.HAUTEUR_ECRAN_METRE - heros.taille:
        heros.y = Game.HAUTEUR_ECRAN_METRE - heros.taille


    # Supprimer les personnages morts.
    for personnage in Game.personnages:
        if not personnage.vivant:
            personnage.supprimer()
