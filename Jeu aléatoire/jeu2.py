from neurone import *
from random import randint
from time import sleep

lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class JeuAleatoire:
    def __init__(self, nbr_variables=10, nbr_touches=2):
        self.reseau = Reseaux([Perceptron() for i in range(nbr_variables+nbr_touches)],
                              [Sortie(lambda x:x) for _ in range(nbr_variables)],
                              1, nbr_variables+nbr_touches)

        self.variables = self.reseau.entrees[:-nbr_touches]
        self.sorties = self.reseau.sorties
        for variable in self.variables:
            variable.valeur = randint(-100, 100)
        assert len(self.sorties) == len(self.variables), "Les tailles sont différentes."
        
        self.var_touches = self.reseau.entrees[-nbr_touches:]
        for touche in self.var_touches:
            touche.valeur = 0
        

    def update(self):
        self.reseau.update()
        for i in range(len(self.variables)):
            v = self.variables[i]
            v.valeur = (self.sorties[i].valeur*10)
            v.valeur = v.valeur
            v.valeur = -100 if v.valeur < -100 else v.valeur
            v.valeur = 100 if v.valeur > 100 else v.valeur


    def afficher(self):
        for variable in self.variables:
            print(variable.valeur)

if __name__ == "__main__":
    J = JeuAleatoire()
    for _ in range(1000):
        J.update()
        J.afficher()
        print("-"*15)
        sleep(1)















































