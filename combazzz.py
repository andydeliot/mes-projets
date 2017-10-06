
from functools import total_ordering
from math import ceil
from copy import deepcopy

def asserteur(variable, type_variable):
    assert type(variable) is type_variable, "La variable donné n'est pas de type {0} ({1}:{2})".format(type_variable, type(variable), variable)

class Fourmi:
    def __init__(self, fourmilliere, nombre, emplacement="Terrain de chasse"):
        asserteur(fourmilliere, Fourmilliere)
        asserteur(nombre, int)
        assert nombre >= 0, "Le nombre de fourmis doit être supérieur à 0 : " + str(nombre)
        fourmilliere.assert_emplacement(emplacement)

        self.fourmilliere = fourmilliere
        self.fourmilliere.armees.append(self)

        self.nombre = nombre
        self.emplacement = emplacement

        if self.emplacement == "Terrain de chasse":
            bonus_defense = 1.
        elif self.emplacement == "Dome":
            bonus_defense = 1.10 + self.fourmilliere.dome * 0.05
        elif self.emplacement == "Loge":
            bonus_defense = 1.30 + self.fourmilliere.loge * 0.15
        else:
            Exception("L'emplacement n'existe pas. (Terrain de chasse, Dome, Loge)")
        self.bonus_defense = bonus_defense

        self.vie = self.point_vie()

    def subir(self, degat):
        """ Retire des pvs aux fourmis et retourne le nombre de dégat non absorbé. """
        assert degat >= 0, "Les dégats sont négatifs."
        if degat >= self.vie:
            degat -= self.vie
            self.vie = 0
            self.nombre = 0
            self.fourmilliere.armees.remove(self)
            return degat
        else:
            self.vie -= degat
            self.nombre = ceil(self.vie / self.__class__.VIE)
            return 0

    def point_vie(self):
        """ Retourne le nombre de points de vie totale. """
        return self.__class__.VIE * self.bonus_defense * self.nombre

    def point_attaque(self):
        """ Retourne le nombre de points d'attaque. """
        return round(self.__class__.ATTAQUE * (1 + self.fourmilliere.arme * 0.1) * self.nombre)

    def point_defense(self):
        """ Retourne le nombre de points d'attaque. """
        return round(self.__class__.DEFENSE * (1 + self.fourmilliere.defense * 0.1) * self.nombre)

    def __repr__(self):
        return self.__class__.NOM + " (" + str(self.nombre) + ")"

class JeuneSoldateNaine(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 8, 3, 2, 16, 300
    NOM = "Jeune soldate naine"

class SoldateNaine(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 10, 5, 4, 20, 450
    NOM = "soldate naine"

class NaineElite(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 13, 7, 6, 26, 570
    NOM = "Naine d'élite"

class JeuneSoldate(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 16, 10, 9, 30, 740
    NOM = "Jeune soldate"

class Soldate(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 20, 15, 14, 36, 1000
    NOM = "Soldate"

class SoldateElite(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 27, 24, 23, 44, 1450
    NOM = "soldate d'élite"

class Artilleuse(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 10, 30, 15, 30, 1440
    NOM = "Artilleuse"

class ArtilleuseElite(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 12, 35, 18, 34, 1520
    NOM = "Artilleuse d'élite"

class Concierge(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 30, 1, 25, 70, 1410
    NOM = "Concierge"

class Tank(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 35, 55, 1, 100, 1860
    NOM = "Tank"

class Tueuse(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 50, 50, 50, 80, 2740
    NOM = "Tueuse"

class TueuseElite(Fourmi):
    VIE, ATTAQUE, DEFENSE, NOURRITURE, TEMPS = 55, 55, 55, 90, 2740
    NOM = "Tueuse d'élite"


class Fourmilliere:
    EMPLACEMENTS = ["Terrain de chasse", "Dome", "Loge"]
    def __init__(self, nom="Une fourmilliere", vitesse_de_ponte=0, arme=0, defense=0, dome=0, loge=0):
        self.vitesse_de_ponte = vitesse_de_ponte
        self.arme = arme
        self.defense = defense
        self.dome = dome
        self.loge = loge
        self.armees = []

    def assert_emplacement(self, emplacement):
        """ Vérifie que l'emplacement existe. """
        assert emplacement in Fourmilliere.EMPLACEMENTS, "L'emplacement {0} indiqué n'existe pas ({1})".format(emplacement, Fourmilliere.EMPLACEMENTS)

    def combattre(self, fourmilliere, emplacement, *armees_attaque):
        self.assert_emplacement(emplacement)
        while True:
            armees_attaque = [fourmis for fourmis in armees_attaque if fourmis.nombre > 0]
            armees_defense = [fourmis for fourmis in fourmilliere.armees if fourmis.emplacement == emplacement]
            if not (len(armees_attaque) and len(armees_defense)):
                break

            degat_attaque = sum([fourmis.point_attaque() for fourmis in armees_attaque])
            degat_defense = sum([fourmis.point_defense() for fourmis in armees_defense])
            for armee in armees_defense:
                degat_attaque = armee.subir(degat_attaque)
            for armee in armees_attaque:
                degat_defense = armee.subir(degat_defense)

        # Régénération des troupes.
        for armee in armees_attaque:
            armee.vie = armee.point_vie()
        for armee in armees_defense:
            armee.vie = armee.point_vie()

    def attaquer(self, fourmilliere, emplacement, *armees_attaque):
        self.assert_emplacement(emplacement)
        for emplacement_fourmilliere in Fourmilliere.EMPLACEMENTS:
            self.combattre(fourmilliere, emplacement_fourmilliere, *armees_attaque)
            if emplacement_fourmilliere == emplacement:
                break

    def copier(self):
        return deepcopy(self)




if __name__ == "__main__":
    f1 = Fourmilliere()
    Soldate(f1, 50)
    f2 = Fourmilliere()
    Soldate(f2, 10)
    Soldate(f2, 10, "Dome")

    f1.attaquer(f2, "Dome", *f1.armees)
































