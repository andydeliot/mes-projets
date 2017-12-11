

from Game import Game
from Objet import Objet
from Personnage import Personnage
from Texte import TexteEcran


from pygame import *

from time import time
from random import randint



def ia_ennemi(self):
    self.avancer_vers(perso1)

def ia_mega_ennemi(self):
    self.avancer_vers(perso2)

# Objet.
perso1 = Personnage(50, 10, taille=1.5, vitesse=12, nom="Runner (A)")
perso2 = Personnage(10, 50, taille=1.5, vitesse=12, nom="Blocker (Z)")
perso1.selectionner, perso2.selectionner = True, False
perso1.objectifs, perso2.objectifs = [], []
selection = perso1
heros = [perso1, perso2]

# Chrono.
temps_minerai = time()
temps_ennemi = time()
temps_mega_ennemi = time()

# Score.
minerai = 0
ennemi_tue = 0

# Texte.
texte_score = TexteEcran(Game.CENTREX, Game.HAUTEUR_ECRAN - 20, "Minerai : 0  Ennemi tué : 0")

while Game.jouer():

    # Chrono.
    if time() - temps_minerai > 3:
        Objet(randint(0, int(Game.LARGEUR_ECRAN_METRE)), randint(0, int(Game.HAUTEUR_ECRAN_METRE)),
              couleur=(0, 255, 255), taille=0.5)
        temps_minerai = time()

    if time() - temps_ennemi > 5:
        creation = True
        while creation:
            x = randint(0, int(Game.LARGEUR_ECRAN_METRE))
            y = randint(0, int(Game.HAUTEUR_ECRAN_METRE))
            creation = False
            for perso in heros:
                if perso.distance_avec((x, y)) < 50:
                    creation = True
        un_ennemi = Personnage(x, y, couleur=(255, 0, 0), taille=1, nom="Ennemi", nom_ia=ia_ennemi)
        temps_ennemi = time()

    if time() - temps_mega_ennemi > 15:
        Personnage(randint(0, int(Game.LARGEUR_ECRAN_METRE)), randint(0, int(Game.HAUTEUR_ECRAN_METRE)),
                   couleur=(255, 0, 0), vitesse=2, taille=2, nom="MegaEnnemi", nom_ia=ia_mega_ennemi)
        temps_mega_ennemi = time()

    # Minerai.
    for objet in list(Game.objets):
        if objet.couleur == (0, 255, 255):
            if perso1.collision_avec(objet):
                objet.supprimer()
                minerai += 1

    # Collision ennemi.
    for personnage in list(Game.personnages):
        if personnage is not perso1 and personnage is not perso2:
            if perso1.collision_avec(personnage):
                perso1.pv = 0
            if perso2.collision_avec(personnage):
                if personnage.nom == "Ennemi":
                    personnage.supprimer()
                    ennemi_tue += 1
                else:
                    perso2.pv = 0

    # Collision entre ennemi.
    for personnage1 in list(Game.personnages):
        for personnage2 in list(Game.personnages):
            if personnage1 is not personnage2:
                if personnage1 not in heros and personnage2 not in heros:
                    if personnage1.collision_avec(personnage2):
                        if personnage1.nom == "MegaEnnemi" and personnage2.nom == "MegaEnnemi":
                            personnage1.supprimer()
                            personnage2.supprimer()

                        if personnage1.nom == "Ennemi" and personnage2.nom == "Ennemi":
                            personnage1.vitesse += 0.01

    # Selection.
    if Game.bouton_appuye(K_a):
        selection = perso1
    if Game.bouton_appuye(K_z):
        selection = perso2

    if Game.clic_gauche():
        if perso1.collision_avec(Objet.position_logique(Game.position_souris())):
            selection = perso1
        if perso2.collision_avec(Objet.position_logique(Game.position_souris())):
            selection = perso2

    # Couleur sélection.
    for perso in heros:
        perso.couleur = (0, 175, 255) if selection == perso else (0, 0, 255)

    # Controle.
    if Game.clic_droit():
        # Définir l'objectif.
        objectif = Objet.position_logique(Game.position_souris())
        for personnage in Game.personnages:
            if personnage.est_clique():
                objectif = personnage
        # Ajout ou modification de l'objectif.
        if Game.bouton_appuye(K_LSHIFT):
            selection.objectifs.append(objectif)
        else:
            selection.objectifs = [objectif]

    # Déplacement des personnage joueurs.
    for perso in heros:
        if perso.vivant:
            if len(perso.objectifs):
                perso.avancer_vers(perso.objectifs[0])
                if perso.distance_avec(perso.objectifs[0]) < 1:
                    perso.objectifs.pop(0)

    if not perso1.vivant:
        Game.COULEUR_FOND_ECRAN = (25, 0, 0)

    # Affichage des déplacements.
    for perso in heros:
        if len(perso.objectifs):
            couleur_objectif = (0, 75, 0) if selection == perso else (0, 25, 0)
            perso.dessiner_ligne(perso, perso.objectifs[0], couleur_objectif)
            n = 1
            while n < len(perso.objectifs):
                perso.dessiner_ligne(perso.objectifs[n-1], perso.objectifs[n], couleur_objectif)
                n += 1

    # Texte.
    texte_score.texte = "Minerai : {0}  Ennemi tué : {1}".format(minerai, ennemi_tue)












