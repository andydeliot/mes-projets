
from Pygamebuilder.Game import Game
from Pygamebuilder.Objet import Objet

import pygame
from pygame import *


class Item:
    items = []
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.objet = Objet()
        self.couleur = (255, 255, 255)
        self.disque = Objet(taille=0.5)
        Item.items.append(self)

    def update(self):
        self.objet.couleur = (0, 255, 0) if self.calculer() else (255, 0, 0)
        self.disque.couleur = self.couleur
        for fil in self.outputs:
            Objet.dessiner_ligne(self.objet, fil.objet, self.objet.couleur)

    def supprimer(self):
        for fil in self.inputs:
            fil.outputs.remove(self)
        for fil in self.outputs:
            fil.inputs.remove(self)
        self.outputs = []
        self.inputs = []
        
        self.objet.supprimer()
        self.disque.supprimer()
        Item.items.remove(self)

class Interrupteur(Item):
    def __init__(self):
        Item.__init__(self)
        self.couleur = (255, 255, 0)
        self.etat = False

    def calculer(self):
        return self.etat

class And(Item):
    def __init__(self):
        Item.__init__(self)
        self.couleur = (255, 0, 255)

    def calculer(self):
        if not len(self.inputs):
            return False
        for item in self.inputs:
            if not item.calculer():
                return False
        return True

class Or(Item):
    def __init__(self):
        Item.__init__(self)
        self.couleur = (0, 255, 255)

    def calculer(self):
        if not len(self.inputs):
            return False
        for item in self.inputs:
            if item.calculer():
                return True
        return False

class Non(Item):
    def __init__(self):
        Item.__init__(self)
        self.couleur = (255, 255, 255)

    def calculer(self):
        if not len(self.inputs):
            return False
        return not self.inputs[0].calculer()

class Resultat(Item):
    def __init__(self):
        Item.__init__(self)
        self.couleur = (0, 0, 0)

    def calculer(self):
        if not len(self.inputs):
            return False
        return self.inputs[0].calculer()


def creer(classe, x, y):
    i = classe()
    i.objet.x = x
    i.objet.y = y
    i.disque.x = x
    i.disque.y = y

etat = "Interrupteur"

my_input = ""
my_output = ""

while Game.jouer():

    if Game.bouton_appuye(K_a):
        etat = "Interrupteur"
    elif Game.bouton_appuye(K_z):
        etat = "And"
    elif Game.bouton_appuye(K_e):
        etat = "Or"
    elif Game.bouton_appuye(K_r):
        etat = "Non"
    elif Game.bouton_appuye(K_t):
        etat = "Resultat"
    elif Game.bouton_appuye(K_w):
        etat = "Fil"

    if Game.clic_gauche():
        for item in Item.items:
            if item.objet.est_clique():
                if item.__class__ is Interrupteur:
                    item.etat = not item.etat

                if etat == "Fil":
                    my_input = item

        vide = True
        for item in Item.items:
            if item.objet.est_clique():
                vide = False
        if vide:
            if etat == "Interrupteur":
                classe = Interrupteur
            elif etat == "And":
                classe = And
            elif etat == "Or":
                classe = Or
            elif etat == "Non":
                classe = Non
            elif etat == "Resultat":
                classe = Resultat
            if etat != "Fil":
                creer(classe, *Objet.position_logique(Game.position_souris()))

    if Game.declic_gauche():
        for item in Item.items:
            if item.objet.touche_position(Objet.position_logique(Game.position_souris())):
                my_output = item
        try:
            assert type(my_input) is not str, "Erreur de type"
            assert type(my_output) is not str, "Erreur de type"
            my_input.outputs.append(my_output)
            my_output.inputs.append(my_input)
        except:
            pass
        my_input = ""
        my_output = ""

    if Game.clic_droit():
        for item in Item.items:
            if item.objet.est_clique():
                item.supprimer()

    for item in Item.items:
        item.update()

    


















        
