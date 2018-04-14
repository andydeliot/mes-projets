
import math
from random import randrange


class Lien:
    def __init__(self, entree, sortie):
        self.entree = entree
        self.sortie = sortie
        self.valeur = randrange(-10, 10) / 100.

        self.apprentissage = 0.1

        self.entree.sorties.append(self)
        self.sortie.entrees.append(self)

    def correction_valeur(self):
        self.valeur = self.valeur + (self.apprentissage * self.entree.valeur * self.sortie.delta)


class Perceptron:
    def __init__(self, updateur):
        self.updateur = updateur
        self.valeur = 0

        self.sorties = []
        
    def update(self):
        self.valeur = self.updateur()


class Sortie:
    def __init__(self, procedure):
        self.procedure = procedure
        self.valeur = 0
        self.delta = 0

        self.entrees = []

    def update(self):
        x = sum([l.entree.valeur * l.valeur for l in self.entrees])
        x = -100 if x < -100 else x
        x = 100 if x > 100 else x
        self.valeur = 1. / (1. + math.exp(-x))

        if self.valeur >= 0.5:
            self.procedure()

    def valeur_delta(self, valeur_souhaite):
        self.delta = valeur_souhaite - self.valeur


class Neurone:
    def __init__(self):
        self.entrees = []
        self.sorties = []
        self.valeur = 0
        self.delta = 0

    def update(self):
        x = sum([l.entree.valeur * l.valeur for l in self.entrees])
        x = -100 if x < -100 else x
        x = 100 if x > 100 else x
        self.valeur = 1. / (1. + math.exp(-x))

    def retropropagation(self):
        somme_sortie = sum([l.sortie.delta * l.valeur for l in self.sorties])
        self.delta = self.valeur * (1 - self.valeur) * somme_sortie 






























