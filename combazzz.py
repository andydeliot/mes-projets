
from functools import total_ordering
from math import ceil


class Fourmi:
    def __init__(self, fourmilliere, nombre, emplacement="Terrain de chasse"):
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
    def __init__(self, vitesse_de_ponte=0, arme=0, defense=0, dome=0, loge=0):
        self.vitesse_de_ponte = vitesse_de_ponte
        self.arme = arme
        self.defense = defense
        self.dome = dome
        self.loge = loge
        self.armees = []

    def attaquer(self, fourmilliere, emplacement, *armees_attaque):
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

##
##class Troupe:
##    def __init__(self, fourmi, nombre, vie=None):
##        self.fourmi = fourmi
##        self.nombre = nombre if nombre > 0 else 0
##
##        if vie is None:
##            self.vie = self.fourmi.VIE * self.nombre
##        else:
##            self.vie = vie
##        self.attaque = self.fourmi.ATTAQUE * self.nombre
##        self.defense = self.fourmi.DEFENSE * self.nombre
##        self.temps = self.fourmi.TEMPS * self.nombre
##        self.nourriture = self.fourmi.NOURRITURE * self.nombre
##
##    def egale(self, other):
##        assert type(other) is Troupe, "Le comparateur n'est pas de type Troupe."
##        return True if self.fourmi is other.fourmi and self.nombre == other.nombre else False
##
##    def subi(self, degat):
##        """ Retourne la troupe avec le nouveau nombre de fourmis, et son nouveau nombre de points de vie. """
##        vie = self.vie - degat
##        nombre = ceil(vie / self.fourmi.VIE)
##        return Troupe(self.fourmi, nombre, vie)
##
##    def __repr__(self):
##        return self.fourmi.NOM + "(" + str(self.nombre) + ")"
##
##
##@total_ordering
##class Armee:
##    def __init__(self, *troupes, bonus=1):
##        self.troupes = [Troupe(troupe.fourmi, int(troupe.nombre), troupe.vie) for troupe in troupes if troupe.nombre > 0]
##
##        # Statistiques.
##        self.vie = 0
##        self.attaque = 0
##        self.defense = 0
##        self.temps = 0
##        self.nourriture = 0
##        for troupe in self.troupes:
##            self.vie += troupe.vie
##            self.attaque += troupe.attaque
##            self.defense += troupe.defense
##            self.temps += troupe.temps
##            self.nourriture += troupe.nourriture
##
##    def egale(self, other):
##        assert type(other) is Armee, "Le comparateur n'est pas de type Armee."
##        if len(self.troupes) != len(other.troupes): return False
##        i = 0
##        while True:
##            if i >= len(self.troupes): break
##            if not self.troupes[i].egale(other.troupes[i]): return False
##            i += 1
##        return True
##
##    def __eq__(self, other):
##        assert type(other) is Armee, "Impossible de comparé autre chose qu'une armée."
##        attaquante1, defenseuse1 = self.combattre(other)
##        attaquante2, defenseuse2 = other.combattre(self)
##        return attaquante1.temps + defenseuse2.temps == defenseuse1.temps + attaquante2.temps
##
##    def __gt__(self, other):
##        assert type(other) is Armee, "Impossible de comparé autre chose qu'une armée."
##        attaquante1, defenseuse1 = self.combattre(other)
##        attaquante2, defenseuse2 = other.combattre(self)
##        return attaquante1.temps + defenseuse2.temps > defenseuse1.temps + attaquante2.temps
##
##    def vivante(self):
##        """ Retourne vrai si l'armée n'est pas vide de troupes. """
##        return self.troupes != []
##
##    def combattre(self, armee, printer=False):
##        """ Fait combatre les deux armées. Retourne également les deux armées, l'armée attaquante en premiere position. """
##        if printer: print("-"*90)
##        armee_attaque = self
##        armee_defense = armee
##        while armee_attaque.vivante() and armee_defense.vivante():
##            if armee_attaque.attaque >= armee_defense.vie * 3:
##                coef_defense = 0.1
##            elif armee_attaque.attaque >= armee_defense.vie * 2:
##                coef_defense = 0.3
##            elif armee_attaque.attaque >= armee_defense.vie * 1.5:
##                coef_defense = 0.5
##            else:
##                coef_defense = 1
##            armee_defense_temp = armee_attaque.attaquer(armee_defense, armee_attaque.attaque, printer)
##            armee_attaque = armee_defense.attaquer(armee_attaque, armee_defense.defense*coef_defense, printer)
##            armee_defense = armee_defense_temp
##            if printer: print("")
##
##        if printer: print(armee_attaque, armee_defense)
##        return armee_attaque, armee_defense
##
##    def attaquer(self, armee, degat, printer=False):
##        """ Retourne l'armée attaqué. """
##        if printer:
##            print(self)
##            print("Les attaquantes infligent {0} points de dégats.".format(degat))
##
##        troupes = []
##        for troupe in armee.troupes:
##            new_troupe = troupe.subi(degat)
##            degat = -new_troupe.vie if new_troupe.vie < 0 else 0
##
##            troupes.append(new_troupe)
##            if printer:
##                print("Les défenseuses perdent {0} {1}. ({2} pv)".format(troupe.nombre - new_troupe.nombre, new_troupe.fourmi.NOM, new_troupe.vie))
##
##        return Armee(*troupes)
##
##    def attaque_temps(self, armee):
##        """ Retourne le temps final lorsque l'armée attaque une autre armée. """
##        armee_final, _ = self.combattre(armee)
##        print(armee_final.temps)
##        return armee_final.temps
##
##    def defense_temps(self, armee):
##        """ Retourne le temps final lorsque l'armée attaque une autre armée. """
##        _, armee_final = armee.combattre(self)
##        print(armee_final.temps)
##        return armee_final.temps
##
##    def difference(self, armee):
##        """ Retourne une armée représentant la différence entre les deux armées. Les deux armées doivent avoir les même types de troupes. """
##        for troupe in armee.troupes:
##            assert troupe.fourmi in [troupe.fourmi for troupe in self.troupes], "La troupe de l'armée n'existe pas"
##
##        troupes = []
##        for troupe in armee.troupes:
##            for troupe2 in self.troupes:
##                if troupe.fourmi is troupe2.fourmi:
##                    troupes.append(Troupe(troupe.fourmi, troupe2.nombre - troupe.nombre))
##
##        return Armee(*troupes)
##
##    def __repr__(self):
##        return str(self.troupes)
##
##
##
##jsn = Fourmi("Jeune soldate naine", 8, 3, 2, 22, 16)
##sn = Fourmi("Soldate naine", 10, 5, 4, 32, 20)
##ne = Fourmi("Naine d'élite", 13, 7, 6, 41, 26)
##js = Fourmi("Jeune soldate", 16, 10, 9, 53, 30)
##s = Fourmi("Soldate", 20, 15, 14, 72, 36)
##c = Fourmi("Concierge", 30, 1, 25, 101, 70)
##a = Fourmi("Artilleuse",10, 30, 15, 103, 30)
##ae = Fourmi("Artilleuse d'élite", 12, 35, 18, 109, 34)
##se = Fourmi("Soldate d'élite", 27, 24, 23, 104, 44)
##t = Fourmi("Tank", 35, 55, 1, 134, 100)
##tu = Fourmi("Tueuse", 50, 50, 50, 197, 80)
##tue = Fourmi("Tueuse d'élite", 55, 55, 55, 197, 90)
##
##fourmis = [jsn, sn, ne, js, s, c, a, ae, se, t, tu, tue]
##
##
##def statistiques():
##    print(fourmis)
##    print("")
##
##    fourmis_nombre = sorted(fourmis, key=lambda f: f.nombre_par_recolte, reverse=True)
##    print("Nombre :", fourmis_nombre)
##
##    fourmis_vie = sorted(fourmis, key=lambda f: f.vie_par_recolte, reverse=True)
##    print("Vie :", fourmis_vie)
##
##    fourmis_attaque = sorted(fourmis, key=lambda f: f.attaque_par_recolte, reverse=True)
##    print("Attaque :", fourmis_attaque)
##
##    fourmis_defense = sorted(fourmis, key=lambda f: f.defense_par_recolte, reverse=True)
##    print("Défense :", fourmis_defense)
##
##    fourmis_nourriture = sorted(fourmis, key=lambda f: f.nourriture_par_recolte, reverse=True)
##    print("Nourriture :", fourmis_nourriture)
##
##    fourmis_combat = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte)) for fourmi in fourmis]
##    fourmis_combat = sorted(fourmis_combat)
##    print("Combat entre elles :", fourmis_combat)
##    
##    fourmis_combat_temps = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte*10)) for fourmi in fourmis]
##    fourmis_combat_temps = sorted(fourmis_combat_temps, key=lambda a: a.attaque_temps(Armee(Troupe(c, 100))))
##    print("Combat temps :", fourmis_combat_temps)
##
##    fourmis_defense_temps = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte*10)) for fourmi in fourmis]
##    fourmis_defense_temps = sorted(fourmis_defense_temps, key=lambda a: a.defense_temps(Armee(Troupe(jsn, 1000))))
##    print("Defense temps :", fourmis_defense_temps)
##
##
##def combat_uni_unite(armee):
##    for f in fourmis:
##        pass
##
##
##if __name__ == "__main__":
####    armee1 = Armee(Troupe(jsn, 1000), Troupe(a, 500))
####    armee2 = Armee(Troupe(c, 300), Troupe(s, 500))
####
####    armee3 = armee1.combattre(armee2, printer= True)
####
####    mon_armee = Armee(Troupe(jsn, 2493), Troupe(se, 502), Troupe(ne, 338), Troupe(js, 2000), Troupe(a, 382))
####
####    statistiques()
##
##    mon_armee = Armee(Troupe(js, 3000), Troupe(s, 900), Troupe(a, 4500))
##    guigui0025 = Armee(Troupe(jsn, 500), Troupe(sn, 500), Troupe(ne, 500), Troupe(js, 500))
##    petitionner = Armee(Troupe(jsn, 99), Troupe(sn, 967), Troupe(ne, 2859))
##    zarby89 = Armee(Troupe(jsn, 2238), Troupe(sn, 753), Troupe(ne, 398))
##
##    mon_armee.combattre(guigui0025, printer=True)
##    mon_armee.combattre(petitionner, printer=True)
##    mon_armee.combattre(zarby89, printer=True)
##    
##
##    ma_defense = Armee(Troupe(jsn, 2400), Troupe(sn, 500), Troupe(ne, 338), Troupe(se, 171))
##    guigui0025.combattre(ma_defense, True)
##    petitionner.combattre(ma_defense, True)
##    zarby89.combattre(ma_defense)
##
##
##
##
##

























