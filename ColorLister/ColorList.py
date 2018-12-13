

from PIL import Image
from itertools import combinations
from math import ceil

class Listeur:
    def __init__(self, taille_icone=150, marge=5, couleur_fond=(255, 255, 255)):
        taille = ceil(220 ** 0.5) * taille_icone
        self.image = Image.new("RGB", (taille, taille), couleur_fond)
        self.taille_icone = taille_icone
        self.marge = marge

    def run(self, combinaisons):
        x = 0
        y = 0
        while y < self.image.height:
            try:
                combinaison = combinaisons.__next__()
            except StopIteration:
                break
            self.dessiner_figure(x, y, *combinaison)
            x += self.taille_icone
            if x >= self.image.width:
                x = 0
                y += self.taille_icone

        self.image.save("ColorList.png")

    def dessiner_rectangle(self, x, y, couleur, longueurx, longueury):
        """ Dessine un carré. """
        for a in range(longueurx):
            for b in range(longueury):
                self.image.putpixel((x+a,y+b), couleur)

    def dessiner_figure(self, x, y, couleur1, couleur2, couleur3):
        """ Dessine une figure dans un carré de 100 par 100. """
        longueur1 = int(self.taille_icone - (self.marge*2))
        hauteur1 = int((self.taille_icone - (self.marge*2)) / 3)
        longueur2 = int((self.taille_icone - (self.marge*2)) / 2)
        hauteur2 = int((self.taille_icone - (self.marge*2)) / 3 * 2)

        x += self.marge
        y += self.marge
        self.dessiner_rectangle(x, y, couleur1, longueur1, hauteur1)

        y += hauteur1
        self.dessiner_rectangle(x, y, couleur2, longueur2, hauteur2)

        x += longueur2
        self.dessiner_rectangle(x, y, couleur3, longueur2, hauteur2)




if __name__ == "__main__":

    couleurs = [(195, 47, 129), # Fushia
                (255, 46, 60), # Rouge
                (224, 101, 50), # Orange
                (224, 205, 66), # Jaune
                (191, 210, 96), # Vert citron
                (55, 179, 127), # Vert
                (30, 192, 238), # Turquoise
                (40, 62, 116), # Bleu
                (102, 44, 112), # Violet
                (152, 45, 119), # Violette
                (169, 102, 35), # Café
                (21, 21, 19)] # Noir
    combinaisons = combinations(couleurs, 3)

    l = Listeur()
    l.run(combinaisons)














    


