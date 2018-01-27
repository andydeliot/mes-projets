# coding=utf-8

import pygame
try:
    from Pygamebuilder.Game import Game
    from Pygamebuilder.Objet import Objet
    from Pygamebuilder.Texte import TexteObjet, TexteEcran
except:
    from Game import Game
    from Objet import Objet
    from Texte import TexteObjet, TexteEcran


class BoutonObjet(Objet):
    """ Bouton collé a une position ou un objet. """

    def __init__(self, x=10, y=10, texte="Cliquez moi", taille_texte=20, couleur=(0, 200, 0)):
        Objet.__init__(self, x, y, taille_texte, 0, 0, 0, couleur)
        self.texte = texte
        self.taille_texte = taille_texte
        self.TexteObjet = TexteObjet(x, y, self.texte, taille=self.taille_texte)
        self.largeur, self.hauteur = self.TexteObjet.render.get_rect()[2] / 2 + 5, self.TexteObjet.render.get_rect()[3] / 2 + 5

    def update(self):
        self.TexteObjet.x, self.TexteObjet.y = self.x, self.y
        self.dessiner_rectangle(self, self.largeur, self.hauteur, self.couleur)

    def clique(self):
        if Game.clic_gauche():
            position = Game.position_souris()
            xd, yd = Objet.position_graphique((self.x, self.y))
            if xd - self.largeur < position[0] < xd + self.largeur and yd - self.hauteur < position[1] < yd + self.hauteur:
                return True
        return False


class BoutonEcran:
    """ Bouton collé a l'écran. """

    def __init__(self, px=Game.LARGEUR_ECRAN - 100, py=30, texte="Cliquez moi", taille_texte=30, couleur=(0, 200, 0)):
        self.px, self.py = px, py
        self.texte = texte
        self.taille_texte = taille_texte
        self.couleur = couleur
        self.TexteEcran = TexteEcran(self.px, self.py, self.texte, self.taille_texte)
        self.largeur, self.hauteur = self.TexteEcran.render.get_rect()[2] / 2 + 5, self.TexteEcran.render.get_rect()[3] / 2 + 5

        self.affichage = True

        Game.boutons.append(self)

    def update(self):
        if self.affichage:
            pygame.draw.polygon(Game.Ecran, self.couleur,
                                [[self.px - self.largeur, self.py - self.hauteur], [self.px + self.largeur, self.py - self.hauteur],
                                 [self.px + self.largeur, self.py + self.hauteur], [self.px - self.largeur, self.py + self.hauteur]])
            self.TexteEcran.update()

    def clique(self):
        if self.affichage:
            if Game.clic_gauche():
                position = Game.position_souris()
                if self.px - self.largeur < position[0] < self.px + self.largeur and self.py - self.hauteur < position[1] < self.py + self.hauteur:
                    return True
        return False

    def afficher(self):
        self.affichage = True
        self.TexteEcran.afficher()

    def cacher(self):
        self.affichage = False
        self.TexteEcran.cacher()
