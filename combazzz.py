
from functools import total_ordering

temps_recolte = 30 * 60


class Fourmi:
    def __init__(self, nom, vie, attaque, defense, temps, nourriture, nombre=1):
        self.nom = nom

        self.vie = vie
        self.attaque = attaque
        self.defense = defense
        self.temps = temps
        self.nourriture = nourriture

        # Stats.
        self.nombre_par_recolte = temps_recolte / self.temps
        self.vie_par_recolte = self.vie * self.nombre_par_recolte
        self.attaque_par_recolte = self.attaque * self.nombre_par_recolte
        self.defense_par_recolte = self.defense * self.nombre_par_recolte
        self.nourriture_par_recolte = self.nourriture * self.nombre_par_recolte

    def __repr__(self):
        return self.nom


class Troupe:
    def __init__(self, fourmi, nombre):
        self.fourmi = fourmi
        self.nombre = nombre # N'interviens pas dans les stats.

        self.vie = self.fourmi.vie * self.nombre
        self.attaque = self.fourmi.attaque * self.nombre
        self.defense = self.fourmi.defense * self.nombre
        self.temps = self.fourmi.temps * self.nombre
        self.nourriture = self.fourmi.nourriture * self.nombre

    def egale(self, other):
        assert type(other) is Troupe, "Le comparateur n'est pas de type Troupe."
        return True if self.fourmi is other.fourmi and self.nombre == other.nombre else False


    def __repr__(self):
        return self.fourmi.nom + "(" + str(self.nombre) + ")"


@total_ordering
class Armee:
    def __init__(self, *troupes):
        self.troupes = [Troupe(troupe.fourmi, int(troupe.nombre)) for troupe in troupes if troupe.nombre > 0]

        self.vie = 0
        self.attaque = 0
        self.defense = 0
        self.temps = 0
        self.nourriture = 0
        for troupe in self.troupes:
            self.vie += troupe.vie
            self.attaque += troupe.attaque
            self.defense += troupe.defense
            self.temps += troupe.temps
            self.nourriture += troupe.nourriture

    def egale(self, other):
        assert type(other) is Armee, "Le comparateur n'est pas de type Armee."
        if len(self.troupes) != len(other.troupes):
            return False
        i = 0
        while True:
            if i >= len(self.troupes):
                break
            if not self.troupes[i].egale(other.troupes[i]):
                return False
            i += 1
        return True

    def __eq__(self, other):
        assert type(other) is Armee, "Impossible de comparé autre chose qu'une armée."
        attaquante1, defenseuse1 = self.combattre(other)
        attaquante2, defenseuse2 = other.combattre(self)
        return attaquante1.temps + defenseuse2.temps == defenseuse1.temps + attaquante2.temps

    def __gt__(self, other):
        assert type(other) is Armee, "Impossible de comparé autre chose qu'une armée."
        attaquante1, defenseuse1 = self.combattre(other)
        attaquante2, defenseuse2 = other.combattre(self)
        return attaquante1.temps + defenseuse2.temps > defenseuse1.temps + attaquante2.temps

    def vivante(self):
        """ Retourne vrai si l'armée n'est pas vide de troupes. """
        return self.troupes != []

    def combattre(self, armee, printer=False):
        """ Fait combatre les deux armées. Retourne également les deux armées, l'armée attaquante en premiere position. """
        armee_attaque = self
        armee_defense = armee
        while armee_attaque.vivante() and armee_defense.vivante():
            if armee_attaque.attaque >= armee_defense.vie * 3:
                coef_defense = 0.1
            elif armee_attaque.attaque >= armee_defense.vie * 2:
                coef_defense = 0.3
            elif armee_attaque.attaque >= armee_defense.vie * 1.5:
                coef_defense = 0.5
            else:
                coef_defense = 1
            armee_defense_temp = armee_attaque.attaquer(armee_defense, armee_attaque.attaque, printer)
            armee_attaque = armee_defense.attaquer(armee_attaque, armee_defense.defense*coef_defense, printer)
            armee_defense = armee_defense_temp
            if printer: print("")

        if printer: print(armee_attaque, armee_defense)
        return armee_attaque, armee_defense

    def attaquer(self, armee, degat, printer=False):
        """ Retourne l'armée attaqué. """
        if printer:
            print(self)
            print("Les attaquantes infligent {0} points de dégats.".format(degat))

        troupes = []
        for troupe in armee.troupes:
            tue = int(degat / troupe.fourmi.vie)
            tue = troupe.nombre if tue > troupe.nombre else tue

            degat -= tue * troupe.fourmi.vie
            troupes.append(Troupe(troupe.fourmi, troupe.nombre - tue))
            if printer:
                print("Les défenseuses perdent {0} {1}.".format(tue, troupe.fourmi.nom))

        return Armee(*troupes)

    def attaque_temps(self, armee):
        """ Retourne le temps final lorsque l'armée attaque une autre armée. """
        armee_final, _ = self.combattre(armee)
        print(armee_final.temps)
        return armee_final.temps

    def defense_temps(self, armee):
        """ Retourne le temps final lorsque l'armée attaque une autre armée. """
        _, armee_final = armee.combattre(self)
        print(armee_final.temps)
        return armee_final.temps

    def difference(self, armee):
        """ Retourne une armée représentant la différence entre les deux armées. Les deux armées doivent avoir les même types de troupes. """
        for troupe in armee.troupes:
            assert troupe.fourmi in [troupe.fourmi for troupe in self.troupes], "La troupe de l'armée n'existe pas"

        troupes = []
        for troupe in armee.troupes:
            for troupe2 in self.troupes:
                if troupe.fourmi is troupe2.fourmi:
                    troupes.append(Troupe(troupe.fourmi, troupe2.nombre - troupe.nombre))

        return Armee(*troupes)

    def __repr__(self):
        return str(self.troupes)



jsn = Fourmi("Jeune soldate naine", 8, 3, 2, 22, 16)
sn = Fourmi("Soldate naine", 10, 5, 4, 32, 20)
ne = Fourmi("Naine d'élite", 13, 7, 6, 41, 26)
js = Fourmi("Jeune soldate", 16, 10, 9, 53, 30)
s = Fourmi("Soldate", 20, 15, 14, 72, 36)
c = Fourmi("Concierge", 30, 1, 25, 101, 70)
a = Fourmi("Artilleuse",10, 30, 15, 103, 30)
ae = Fourmi("Artilleuse d'élite", 12, 35, 18, 109, 34)
se = Fourmi("Soldate d'élite", 27, 24, 23, 104, 44)
t = Fourmi("Tank", 35, 55, 1, 134, 100)
tu = Fourmi("Tueuse", 50, 50, 50, 197, 80)
tue = Fourmi("Tueuse d'élite", 55, 55, 55, 197, 90)

fourmis = [jsn, sn, ne, js, s, c, a, ae, se, t, tu, tue]


def statistiques():
    print(fourmis)
    print("")

    fourmis_nombre = sorted(fourmis, key=lambda f: f.nombre_par_recolte, reverse=True)
    print("Nombre :", fourmis_nombre)

    fourmis_vie = sorted(fourmis, key=lambda f: f.vie_par_recolte, reverse=True)
    print("Vie :", fourmis_vie)

    fourmis_attaque = sorted(fourmis, key=lambda f: f.attaque_par_recolte, reverse=True)
    print("Attaque :", fourmis_attaque)

    fourmis_defense = sorted(fourmis, key=lambda f: f.defense_par_recolte, reverse=True)
    print("Défense :", fourmis_defense)

    fourmis_nourriture = sorted(fourmis, key=lambda f: f.nourriture_par_recolte, reverse=True)
    print("Nourriture :", fourmis_nourriture)

    fourmis_combat = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte)) for fourmi in fourmis]
    fourmis_combat = sorted(fourmis_combat)
    print("Combat entre elles :", fourmis_combat)
    
    fourmis_combat_temps = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte*10)) for fourmi in fourmis]
    fourmis_combat_temps = sorted(fourmis_combat_temps, key=lambda a: a.attaque_temps(Armee(Troupe(c, 100))))
    print("Combat temps :", fourmis_combat_temps)

    fourmis_defense_temps = [Armee(Troupe(fourmi, fourmi.nombre_par_recolte*10)) for fourmi in fourmis]
    fourmis_defense_temps = sorted(fourmis_defense_temps, key=lambda a: a.defense_temps(Armee(Troupe(jsn, 1000))))
    print("Defense temps :", fourmis_defense_temps)


def combat_uni_unite(armee):
    for f in fourmis:
        pass


if __name__ == "__main__":
    armee1 = Armee(Troupe(jsn, 1000), Troupe(a, 500))
    armee2 = Armee(Troupe(c, 300), Troupe(s, 500))

    armee3 = armee1.combattre(armee2, printer= True)

    mon_armee = Armee(Troupe(jsn, 2493), Troupe(se, 502), Troupe(ne, 338), Troupe(js, 2000), Troupe(a, 382))

    statistiques()






































