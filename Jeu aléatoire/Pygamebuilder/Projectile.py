# coding=utf-8
from math import pi

try:
    from Pygamebuilder.Game import Game
    from Pygamebuilder.Objet import Objet
except ImportError:
    from Game import Game
    from Objet import Objet

class Projectile(Objet):
    """ Un projectile sortant d'une arme sur le terrain. """
    taille = 0.2
    vitesse = 70
    vitesse_angle = 0
    temps_de_vie_max = 1.5
    couleur = (125, 125, 125)
    priorite_affichage = 60

    def __init__(self, personnage):
        Objet.__init__(self, personnage.x, personnage.y, Projectile.taille, Projectile.vitesse, Projectile.vitesse_angle,
                       personnage.angle_vision, Projectile.couleur, Projectile.priorite_affichage)
        self.personnage = personnage
        self.temps_de_vie_max = Projectile.temps_de_vie_max  # Secondes.
        self.temps_de_vie_actuel = 0

        Game.projectiles.append(self)

    def update(self):
        self.deplacement()
        self.update_temps_de_vie()
        self.afficher()

    def deplacement(self):
        angle_radian = self.angle_vision * pi / 180.
        vitesse = self.vitesse * Game.PERIODE  # M/S * S/I
        vx = Objet.cos(angle_radian) * vitesse
        vy = Objet.sin(angle_radian) * vitesse
        self.x += vx
        self.y += vy

    def update_temps_de_vie(self):
        self.temps_de_vie_actuel += Game.PERIODE
        if self.temps_de_vie_actuel > self.temps_de_vie_max:
            self.supprimer()

    def supprimer(self):
        Game.projectiles.remove(self)
        super().supprimer()


class CorpsACorps(Objet):
    """ Un coup sortant d'une arme d'un personnage. """

    def __init__(self, personnage, x, y, taille, distance_max, angle_vision, temps_de_vie_max, couleur=(125, 125, 125), priorite_affichage=60):
        Objet.__init__(self, x, y, taille, 0, angle_vision=angle_vision, couleur=couleur, priorite_affichage=priorite_affichage)
        self.personnage = personnage
        self.temps_de_vie_max = temps_de_vie_max  # Secondes.
        self.temps_de_vie_actuel = 0
        self.distance_max = distance_max

        Game.projectiles.append(self)

    def update(self):
        self.deplacement()
        self.update_temps_de_vie()
        self.afficher()

    def deplacement(self):
        self.x, self.y = self.position_devant(self.personnage, self.personnage.angle_vision,
                                              self.distance_max * (self.temps_de_vie_actuel / self.temps_de_vie_max))

    def update_temps_de_vie(self):
        self.temps_de_vie_actuel += Game.PERIODE
        if self.temps_de_vie_actuel > self.temps_de_vie_max:
            Game.objets.remove(self)
            Game.projectiles.remove(self)
