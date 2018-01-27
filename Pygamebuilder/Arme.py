# coding=utf-8
try:
    from Pygamebuilder.Game import Game
    from Pygamebuilder.Projectile import Projectile
    from Pygamebuilder.Objet import Objet
except ImportError:
    from Game import Game
    from Projectile import Projectile
    from Objet import Objet

from math import pi


class Arme:
    """ Objet transporté par les personnages. Tir des projectiles."""
    def __init__(self, personnage, frequence_utilisation=0.3, munitions_max=-1):
        self.personnage = personnage  # Le soldat a qui appartient l'arme.

        self.frequence_utilisation = frequence_utilisation
        self.temps_derniere_utilisation = self.frequence_utilisation
        self.munitions_max = munitions_max
        self.munitions = self.munitions_max

    def utilisable(self):
        """ Observe si l'arme est utilisable.
        C'est a dire que temps_derniere_utilisation >= frequence_utilisation. et munitions != 0"""
        return True if self.temps_derniere_utilisation >= self.frequence_utilisation and self.munitions != 0 else False

    def utiliser(self):
        """ Fonction à implémenter dans les sous classes. """
        if self.utilisable():
            Projectile(self.personnage)
            self.temps_derniere_utilisation = 0
            self.munitions -= 1

    def utiliser_sur(self, objet):
        #if self.objet_devant_soi(objet):
        self.utiliser()

    def update(self):
        """ Permet de mettre à jour des évenements. """
        self.temps_derniere_utilisation += Game.PERIODE

    # Securité.
    def distance_tir(self):
        projectile = Projectile(self.personnage)
        distance = projectile.vitesse * projectile.temps_de_vie_max
        projectile.supprimer()
        return distance

    def tir_securise(self, objet):
        """ Observe si le soldat peut tirer sans blesser d'alliés.
            Retourne True s'il peut tirer, False sinon."""
        return False if self.objet_devant_soi(objet) or objet is self else True

    def objet_devant_soi(self, objet):
        """ Ne semble pas fonctionner. """
        """ Calcule si un objet est situé devant soi, compte la taille de l'objet et la taille des balles du soldat courrant.
            L'objet ne doit pas superposé le soldat, il doit etre a une distance superieur a la distance de sécurité.
            Dans le cas inverse, la fonction retourneras ''.
            /!\ Ne fonctionne pas sur les points (x,y).
            Retourne un booleen. (True ou False) """
        if self.distance_securite_respecte_avec(objet):
            angle1 = self.personnage.angle_avec(objet)
            z = self.personnage.distance_avec(objet)
            y = objet.taille + Projectile.taille
            x = ((z ** 2) - (y ** 2)) ** 0.5
            alpha = Objet.arc_cos(x / z)
            alpha = alpha * 180 / pi
            angle2 = angle1 + alpha
            angle3 = angle1 - alpha
            vision = self.personnage.angle_vision
            dangle1 = Objet.difference_angle(angle2, vision)
            dangle2 = Objet.difference_angle(angle3, vision)
            # Afin de faire face a la précision, je multiplie par 1000, et je int.
            dangle_final = int((dangle1 + dangle2) * 1000)
            angle_vision = int(abs(angle2 - angle3) * 1000)
            if dangle_final == angle_vision:
                return True
            else:
                return False
        else:
            return False

    def distance_securite_respecte_avec(self, objet):
        """ Calcule si un objet est suffisament loin pour pouvoir tirer en sécurité.
            C'est lorsque deux soldats sont l'un sur l'autre.
            Ou encore, si le soldats est plus proche que la distance de tir maximum.
            Retourne un booleen. (True ou False) """
        return self.personnage.distance_avec(objet) > self.distance_tir() and self.personnage.collision(objet)

