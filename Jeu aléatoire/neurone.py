
import math
from random import randrange


class Lien:
    def __init__(self, entree, sortie):
        self.entree = entree
        self.sortie = sortie
        # Valeur aléatoire des liens lors de leur création.
        self.valeur = randrange(-100, 100) / 1000.

        self.apprentissage = 0.1

        self.entree.sorties.append(self)
        self.sortie.entrees.append(self)

    def correction_valeur(self):
        self.valeur = self.valeur + (self.apprentissage * self.entree.valeur * self.sortie.delta)

    def __repr__(self):
        return "{0}({1}) -- {2} -- {3}({4})".format(self.entree.__class__.__name__,
                                                  id(self.entree),
                                                  self.valeur,
                                                  self.sortie.__class__.__name__,
                                                  id(self.sortie))


class Perceptron:
    def __init__(self, updateur=lambda x,**kwargs:x.valeur):
        """ Attention, la signature est trompeuse ! """
        self.updateur = updateur
        self.valeur = 0

        self.sorties = []
        
    def update(self, **kwargs):
        """ Il faut absolument un updateur pour rendre les réseau intéréssant. """
        self.valeur = self.updateur(self, **kwargs)


class Sortie:
    def __init__(self, procedure=lambda x,**kwargs:print(x.valeur)):
        """ Attention, la signature est trompeuse ! """
        self.procedure = procedure
        self.valeur = 0
        self.delta = 0

        self.entrees = []

    def update(self, **kwargs):
        x = sum([l.entree.valeur * l.valeur for l in self.entrees])
##        x = -100 if x < -100 else x
##        x = 100 if x > 100 else x
        self.valeur = x #1. / (1. + math.exp(-x))
        # La valeur est comprise entre 0 et 1. Si x = 0, y = 0.5.

        self.procedure(self, **kwargs)

    def valeur_delta(self, valeur_souhaite):
        """ Fonction utile à la rétro propagation :
            Indiquer la valeur qu'aurait dû obtenir la sortie.
            En théorie, la valeur devrait être entre 0 et 1. """
        self.delta = valeur_souhaite - self.valeur


class Neurone:
    def __init__(self):
        self.entrees = []
        self.sorties = []
        self.valeur = 0
        self.delta = 0

    def update(self):
        x = sum([l.entree.valeur * l.valeur for l in self.entrees])
##        x = -100 if x < -100 else x
##        x = 100 if x > 100 else x
        self.valeur = x #1. / (1. + math.exp(-x))
        # La valeur est comprise entre 0 et 1. Si x = 0, y = 0.5.

    def retropropagation(self):
        somme_sortie = sum([l.sortie.delta * l.valeur for l in self.sorties])
        self.delta = self.valeur * (1 - self.valeur) * somme_sortie 


class Reseaux:
    def __init__(self, entrees, sorties, nbr_couches, longueur_couche):
        self.entrees = entrees
        self.sorties = sorties
        # Création des couches de neurones.
        self.couches = []
        for _ in range(nbr_couches):
            couche = []
            for _ in range(longueur_couche):
                couche.append(Neurone())
            self.couches.append(couche)
        # Liaisons des couches.
        for num_couche in range(len(self.couches)):
            couche_entree = self.entrees if not num_couche else self.couches[num_couche-1]
            for neurone in self.couches[num_couche]:
                for neurone_entree in couche_entree:
                    Lien(neurone_entree, neurone)
        for s in self.sorties:
            for neurone_entree in self.couches[-1]:
                Lien(neurone_entree, s)

    def update(self, **kwargs):
        for e in self.entrees:
            e.update(**kwargs)
        for couche in self.couches:
            for n in couche:
                n.update()
        for s in self.sorties:
            s.update(**kwargs)

    def retropropagation(self):
        for e in self.entrees:
            for l in e.sorties:
                l.correction_valeur()
        self.couches.reverse()
        for couche in self.couches:
            for n in couche:
                n.retropropagation()
        for couche in self.couches:
            for n in couche:
                for l in n.sorties:
                    l.correction_valeur()
        self.couches.reverse()



if __name__ == "__main__":
    R = Reseaux([Perceptron()], [Sortie()], 3, 3)

    for _ in range(10):
        R.update()
        R.sorties[0].valeur_delta(1)
        R.retropropagation()

















































