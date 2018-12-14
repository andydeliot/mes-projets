
# Affichage graphique des graphes MPM

# - Récupérer les graphes #
# - Afficher les sommets #
# - Afficher les variables des sommets #
# - Relier les sommets entre eux #
# - Afficher les sommets dans un ordre logique
# - Mettre une flèche, un sens aux arcs


from Projet_jeu_rts import Gphe

from random import randint

import ctypes
import cProfile

import pygame
from pygame import gfxdraw
from pygame import *
from time import time



def creation_ecran():
    """ Permet de créer des écrans adapté à chaque ordinateur. """
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        ecran = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
    except AttributeError:
        ecran = pygame.display.set_mode((1800, 1000))
    return ecran

pygame.init()

ecran = creation_ecran()
LARGEUR_ECRAN, HAUTEUR_ECRAN = ecran.get_width(), ecran.get_height()
CENTREX = LARGEUR_ECRAN / 2
CENTREY = HAUTEUR_ECRAN / 2

# Ecran.
COULEUR_FOND_ECRAN = (0, 0, 0)

# Vitesse de jeu.
HERTZ = 60  # Nombres d'images par secondes.
PERIODE = 1. / HERTZ
clock = pygame.time.Clock()


# Controle.
continuer = True
pygame.key.set_repeat(10, 10)

# Info.
profileur = cProfile.Profile()
profiliation = False
temps_de_boucle = time()
paufination = False

# Textes.
font=pygame.font.Font(None, 24)





class Sommet:
    def __init__(self, tache, x, y, r=75, couleur=(255, 0, 0)):
        self.tache = tache
        self.tache.sommet = self
        self.x = x
        self.y = y
        self.r = r
        self.couleur = couleur

    def update(self, ecran):
        rect = pygame.rect.Rect((self.x-self.r, self.y-self.r),(self.r*2, self.r*2))
        pygame.gfxdraw.rectangle(ecran, rect, self.couleur)
        
        text = font.render(self.tache.nom[:20], 1, (255,255,255))
        ecran.blit(text, (self.x-self.r, self.y-self.r+15))
        
        text = font.render("({})".format(self.tache.duree), 1, (255,255,255))
        ecran.blit(text, (self.x-self.r, self.y-self.r+30))

        text = font.render(str(self.tache.date_plus_tot), 1, (255,255,255))
        ecran.blit(text, (self.x-self.r, self.y+self.r-15))

        text = font.render(str(self.tache.date_plus_tard), 1, (255,255,255))
        ecran.blit(text, (self.x+self.r-15, self.y+self.r-15))

        for successeur in self.tache.successeurs:
            pygame.gfxdraw.line(ecran, self.x, self.y,
                                successeur.sommet.x, successeur.sommet.y,
                                self.couleur)

    def parcour_largeur(self, liste=[]):
        """ Remplis la liste dans l'ordre d'un parcours en largeur. """
        if self not in liste:
            liste.append(self)
        for successeur in self.tache.successeur:
            liste = successeur.sommet.parcour_largeur(liste)
        return liste






sommets = []
sommets.append(Sommet(Gphe.debut, 75, 75))
sommets.append(Sommet(Gphe.fin, LARGEUR_ECRAN-75, HAUTEUR_ECRAN-75))

for tache in Gphe.taches:
    sommets.append(Sommet(tache, randint(tache.date_plus_tot*90, tache.date_plus_tot*100)+75, randint(tache.date_plus_tard*18, tache.date_plus_tard*20)+75))



while continuer:
    clock.tick(HERTZ)
    ecran.fill(COULEUR_FOND_ECRAN)

    for event in pygame.event.get():
        # Le joueur appuye sur Echap.
        if event.type == KEYUP and event.key == K_ESCAPE: continuer = False
        if event.type == QUIT: continuer = False
        # Controler l'état de la souris.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: etat_clic_gauche = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: etat_clic_droit = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: etat_clic_gauche = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3: etat_clic_droit = False


    for sommet in sommets:
        sommet.update(ecran)


    pygame.display.flip()


if profiliation:
    profileur.disable()
    profileur.create_stats()
    profileur.print_stats()

pygame.quit()













