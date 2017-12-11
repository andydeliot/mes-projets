# coding=utf-8

# Voici l'exemple de jeu numéro 1 de Pygamebuilder.

# Le but du jeu est d'éviter que l'objet rouge ne touche l'objet vert.
# L'objet vert suit la souris.
# La barre situé en dessous représente le temps restant avant la fin de la partie.
# Si le joueur se fait toucher par l'objet rouge, il recommence le timing a zero.

from Game import *
from Texte import *


class Exemple1:
    def __init__(self):
        # La position x et y sont en mettre.
        # La vitesse est en metre par seconde.
        # La vitesse de rotation est en degré par seconde.
        # L'angle de vision est en degré.
        objet_rouge = Objet(10, 50, vitesse=50, vitesse_rotation=1000, couleur=(255, 0, 0))
        objet_vert = Objet(0, 0, couleur=(0, 255, 0))

        # Variable de jeu.
        pos = [0, 0]
        temps_non_touche = 0
        temps_max = 10

        texte_win = TexteEcran(px=Game.CENTREX, py=Game.CENTREY, texte="Victoire !", taille=300)
        texte_win.cacher()

        while Game.jouer():
            # Récuperer la position de la souris.
            if Game.mouvement_souris():
                # Position_logique transforme une position à l'écran (en pixels) en position de jeu (en metres).
                pos = Objet.position_logique(Game.position_souris())

            # Le joueur n'as pas encore gagné.
            if temps_non_touche < temps_max:
                # Positionner l'objet vert sur la souris.
                objet_vert.x = pos[0]
                objet_vert.y = pos[1]

                # Si l'objet rouge est éloigné de 2 metres de l'objet vert, avancer vers celui ci.
                if objet_rouge.distance_avec(objet_vert) > 2:
                    objet_rouge.avancer_vers(pos)

                # Revenir a zero si l'objet rouge touche l'objet vert.
                if objet_vert.collision_avec(objet_rouge):
                    Game.COULEUR_FOND_ECRAN = (20, 0, 0)
                    temps_non_touche = 0
                    objet_rouge.vitesse = 50
                # Sinon, updater le temps de non touché.
                else:
                    Game.COULEUR_FOND_ECRAN = (0, 0, 20)
                    temps_non_touche += Game.PERIODE
                    objet_rouge.vitesse = 50 + 50 * (5 * temps_non_touche / temps_max)
            # Le joueur a gagné.
            else:
                Game.COULEUR_FOND_ECRAN = (0, 20, 0)
                texte_win.afficher()

            # Dessiner une barre sous le joueur représentant le temps non touché par l'objet rouge.
            objet_vert.dessiner_barre(1, 50, temps_non_touche, temps_max, (255, 255, 255))

        Game.quit()

if __name__ == '__main__':
    Exemple1()
    Game.quit()
