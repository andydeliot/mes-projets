# coding=utf-8


class Vision:
    """ Cette classe représente les joueurs. """

    def __init__(self, nom="No name", couleur=(255, 255, 255)):
        self.nom = nom  # Texte.
        # Autre.
        self.zoom = 1  # Niveau de zoom.
        # Position de la vision du joueur.
        self.visionx = 0  # Game.CENTREX
        self.visiony = 0  # Game.CENTREY

        self.couleur = couleur  # RGB.

    def get_vision(self):
        """
        :return: une tuple (self.visionJoueurx, self.visionJoueury)
        """
        return self.visionx, self.visiony
