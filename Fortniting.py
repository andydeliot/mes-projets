
from Pygamebuilder.Game import Game
from Pygamebuilder.Objet import Objet
from Pygamebuilder.Personnage import Personnage
from Pygamebuilder.Arme import Arme
from Pygamebuilder.Projectile import Projectile


from random import randint, choice


import pygame
from pygame import *

from time import time



def ia_choix_position1():
    return randint(0, int(Game.LARGEUR_ECRAN_METRE)), randint(0, int(Game.HAUTEUR_ECRAN_METRE))


ias = []

def ia1(self):
    ennemi_proche = self.objet_le_plus_proche(Game.personnages)
    if ennemi_proche != "":
        if self.distance_avec(ennemi_proche) < 10:
            self.orienter_vers(ennemi_proche)
            self.utiliser_arme_sur(ennemi_proche)
    self.avancer_vers(oeil)
ias.append(ia1)

def ia2(self):
    """ Fuyar """
    ennemi_proche = self.objet_le_plus_proche(Game.personnages)
    if ennemi_proche != "":
        if len(Game.personnages) > 3:
            if self.distance_avec(ennemi_proche) < 15:
                self.orienter_vers(ennemi_proche, 180)
        else:
            if self.distance_avec(ennemi_proche) < 10:
                self.utiliser_arme_sur(ennemi_proche)
    self.avancer_vers(oeil)
ias.append(ia2)


def ia3(self):
    """ Fonceur """
    ennemi_proche = self.objet_le_plus_proche(Game.personnages)
    if ennemi_proche != "":
            self.avancer_vers(ennemi_proche)
            self.utiliser_arme_sur(ennemi_proche)
ias.append(ia3)


class BalleM1(Projectile):
    vitesse = 100
    temps_de_vie_max = 0.1

    def __init__(self, personnage):
        Projectile.__init__(self, personnage)
        self.temps_de_vie_max = BalleM1.temps_de_vie_max
        self.vitesse = BalleM1.vitesse


class M1(Arme):
    degat = 15
    def __init__(self, personnage, frequence_utilisation=0.1, munitions_max=100, projectile=BalleM1):
        Arme.__init__(self, personnage, frequence_utilisation, munitions_max, projectile)
        self.munitions = 30


Game.joueurs = []

class Joueur:
    def __init__(self, ia_choix_position, ia):
        self.ia_choix_position = ia_choix_position
        self.ia = ia
        self.personnage = ""
        self.couleur = (255, 0, 0)
        if self.ia == ia2:
            self.couleur = (0, 255, 0)
        elif self.ia == ia3:
            self.couleur = (0, 0, 255)
        self.choisir_position()

        Game.joueurs.append(self)

    def choisir_position(self):
        x, y = self.ia_choix_position()
        self.personnage = Personnage(x, y, taille = 0.75, vitesse = 3, nom_ia=self.ia, couleur=self.couleur)
        self.personnage.arme_primaire = M1(self.personnage)


for _ in range(10):
    Joueur(ia_choix_position1, choice(ias))

Game.COULEUR_FOND_ECRAN = (75, 0, 30)

oeil = Objet(x=Game.CENTREX_METRE, y=Game.CENTREY_METRE, taille=Game.HAUTEUR_ECRAN_METRE/2, couleur = (255, 255, 255), priorite_affichage=0)
terrain = Objet(x=Game.CENTREX_METRE, y=Game.CENTREY_METRE, taille=Game.LARGEUR_ECRAN_METRE/2, couleur = (0, 0, 0), priorite_affichage=-10, vitesse_rotation=1000,vitesse=5)
temps_cercle = time()
chrono_cercle = 4
niveau = 1

while Game.jouer():

    for personnage in list(Game.personnages):

        # Terrain.
        if personnage.x > Game.LARGEUR_ECRAN_METRE - personnage.taille:
            personnage.x = Game.LARGEUR_ECRAN_METRE - personnage.taille
        if personnage.x < -personnage.taille:
            personnage.x = -personnage.taille
        if personnage.y > Game.HAUTEUR_ECRAN_METRE - personnage.taille:
            personnage.y = Game.HAUTEUR_ECRAN_METRE - personnage.taille
        if personnage.y < -personnage.taille:
            personnage.y = -personnage.taille

        # Balles.
        for projectile in list(Game.projectiles):
            if projectile.personnage is not personnage:
                if projectile.collision_avec(personnage):
                    personnage.pv -= M1.degat
                    projectile.supprimer()
                    if personnage.pv <= 0:
                        projectile.personnage.arme_primaire.munitions += personnage.arme_primaire.munitions

        # Dégat tempete.
        if personnage.distance_avec(terrain) > terrain.taille - personnage.taille:
            personnage.pv -= 10 * niveau * Game.PERIODE

        # Supprimer mort
        if personnage.pv <= 0:
            personnage.supprimer()

    # Cyclone.
    if time() - temps_cercle > chrono_cercle:
        terrain.avancer_vers(oeil)
        terrain.taille *= 0.9998

    if oeil.taille >= terrain.taille:
        oeil.supprimer()
        new_oeil = Objet(x=randint(0, int(Game.LARGEUR_ECRAN_METRE)), y=randint(0, int(Game.HAUTEUR_ECRAN_METRE)), couleur = (255, 255, 255), taille = oeil.taille/2)
        while new_oeil.distance_avec(oeil) > oeil.taille - new_oeil.taille:
            new_oeil.x=randint(0, int(Game.LARGEUR_ECRAN_METRE))
            new_oeil.y=randint(0, int(Game.HAUTEUR_ECRAN_METRE))
        oeil = new_oeil
        temps_cercle = time()
        niveau += 1































        

    


















        
