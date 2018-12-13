# coding=utf-8

import pygame
try:
    from Pygamebuilder.Objet import Objet
    from Pygamebuilder.Game import Game
except:
    from Objet import Objet
    from Game import Game

class TexteObjet(Objet):
    """ Texte collé à une position ou un objet. """

    def __init__(self, x=Game.LARGEUR_ECRAN_METRE / 2, y=Game.HAUTEUR_ECRAN_METRE / 2 + 10, texte="Voici un TexteObjet",
                 taille=20, couleur=(255, 255, 255), font_name="Arial", priorite_affichage=40):
        Objet.__init__(self, x, y, taille, 0, 0, 0, couleur, priorite_affichage)
        self.font = pygame.font.SysFont(font_name, self.taille)

        self.texte = texte
        self.render = self.font.render(self.texte, 1, self.couleur)
        self.text_pos = self.render.get_rect()
        self.text_pos.centerx, self.text_pos.centery = self.x, self.y

    def update(self):
        self.render = self.font.render(self.texte, 1, self.couleur)
        self.text_pos = self.render.get_rect()
        self.text_pos.centerx, self.text_pos.centery = Objet.position_graphique((self.x, self.y))
        self.render = self.font.render(self.texte, 1, self.couleur)
        Game.Ecran.blit(self.render, self.text_pos)


class TexteEcran:
    """ Texte collé a l'écran. """

    def __init__(self, px=Game.CENTREX, py=Game.CENTREY + 200, texte="Voici un TexteEcran", taille=30,
                 couleur=(255, 255, 255), font_name="Arial", alignation="centre"):
        self.px, self.py, self.taille = px, py, taille  # Pixels.
        self.font = pygame.font.SysFont(font_name, self.taille)

        self.texte = texte
        self.couleur = couleur  # RVB
        self.render = self.font.render(str(self.texte), 1, self.couleur)
        self.text_pos = self.render.get_rect()
        self.alignation = alignation
        if self.alignation == "centre":
            self.text_pos.centerx, self.text_pos.centery = self.px, self.py
        if self.alignation == "gauche":
            self.text_pos.left, self.text_pos.centery = self.px, self.py

        self.affichage = True

        Game.textes.append(self)

    def update(self):
        if self.affichage:
            self.render = self.font.render(str(self.texte), 1, self.couleur)
            Game.Ecran.blit(self.render, self.text_pos)

    def afficher(self):
        self.affichage = True

    def cacher(self):
        self.affichage = False
