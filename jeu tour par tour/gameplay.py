
from copy import copy

def distance_echequier(case1, case2):
    return abs(case1.x - case2.x) + abs(case1.y - case2.y)


class Case:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "Case ({0}, {1})".format(self.x, self.y)


class Terrain:
    def __init__(self, taillex, tailley):
        self.cases = []
        for y in range(tailley):
            for x in range(taillex):
                self.cases.append(Case(x, y))

        self.personnages = []
        self.numero_personnage_actif = 0
        self.personnage_actif = None

    def case_libre(self, x, y):
        """ Retourne Vrai si la case est libre. Faux sinon. """
        for case in self.cases:
            if case.x == x and case.y == y:
                for personnage in self.personnages:
                    if personnage.x == x and personnage.y == y:
                        return False
                return True
        return False

    def zonage(self, x, y, portee):
        """ Retourne la liste des cases faisant partie de la zone cible. """
        cases_zone = []
        for case in self.cases:
            if distance_echequier(Case(x, y), case) <= portee:
                cases_zone.append(case)
        return cases_zone

    def start(self):
        """ Débute le jeu. """
        self.personnage_actif = self.personnages[self.numero_personnage_actif]

    def fin_de_tour(self):
        """ Termine le tour du personnage actif et passe au prochain personnage. """
        self.personnage_actif.fin_de_tour()
        self.numero_personnage_actif += 1
        if self.numero_personnage_actif == len(self.personnages):
            self.numero_personnage_actif = 0
        self.personnage_actif = self.personnages[self.numero_personnage_actif]
        self.personnage_actif.debut_de_tour()


class Personnage:
    def __init__(self, terrain, nom, x, y):
        self.terrain = terrain
        self.terrain.personnages.append(self)
        
        self.nom = nom
        self.x = x
        self.y = y

        self.pv = 50
        self.pa = 6
        self.pm = 3

        self.sorts = []
        self.selection_sort = None
        self.etats = []
        self.etats_lances = []

    def get_case(self):
        return Case(self.x, self.y)

    def __str__(self):
        msg = "Personnage {0} en ({1}, {2})".format(self.nom, self.x, self.y)
        msg += " {0} pv, {1} pa, {2} pm".format(self.pv, self.pa, self.pm)
        return msg

    def deplacement_haut(self):
        if self.terrain.case_libre(self.x, self.y-1):
            self.y -= 1
            self.pm -= 1
    def deplacement_bas(self):
        if self.terrain.case_libre(self.x, self.y+1):
            self.y += 1
            self.pm -= 1
    def deplacement_gauche(self):
        if self.terrain.case_libre(self.x-1, self.y):
            self.x -= 1
            self.pm -= 1
    def deplacement_droite(self):
        if self.terrain.case_libre(self.x+1, self.y):
            self.x += 1
            self.pm -= 1

    def selectionner_sort(self, numero=0):
        self.selection_sort = self.sorts[numero]

    def lancer_sort(self, x, y):
        self.selection_sort.run(x, y)

    def debut_de_tour(self):
        for etat in self.etats_lances:
            etat.fin_periode()
            print(etat.duree)

    def fin_de_tour(self):
        self.pa = 6
        self.pm = 3

    def appliquer_sort(self, sort):
        """ Applique le sort subit sur soi-même. """
        copie_sort = sort.copie()
        for etat in self.etats:
            etat.cible_sort(copie_sort)
        for application in copie_sort.applications:
            application(self, copie_sort.personnage)


class Sort:
    def __init__(self, personnage, conditions=[], applications=[]):
        self.personnage = personnage
        self.personnage.sorts.append(self)
        if self.personnage.selection_sort is None:
            self.personnage.selection_sort = self

        self.portee = 0
        self.zone = 0
        self.pa = 0
        self.pm = 0
        for condition in conditions:
            condition(self)

        self.applications = applications

    def run(self, x, y):
        if self.check_conditions(x, y):
            self.run_conditions(x, y)
            cases_zone = self.personnage.terrain.zonage(x, y, self.zone)
            print(cases_zone)
            for case in cases_zone:
                self.run_applications(case.x, case.y)

    def check_conditions(self, x, y):
        if self.personnage.pa < self.pa:
            return False
        if self.personnage.pm < self.pm:
            return False
        if distance_echequier(self.personnage.get_case(), Case(x, y)) > self.portee:
            return False
        return True

    def run_conditions(self, x, y):
        self.personnage.pa -= self.pa
        self.personnage.pm -= self.pm

    def run_applications(self, x, y):
        for personnage in self.personnage.terrain.personnages:
            if personnage.x == x and personnage.y == y:
                personnage.appliquer_sort(self)

    def copie(self):
        """ Retourne une copie du sort avec une nouvelle référence sur les applications. """
        sort = copy(self)
        sort.applications = list(self.applications)
        return sort


def zone(sort):
    sort.zone += 1
def portee(sort):
    sort.portee += 1

def pa(sort):
    sort.pa += 1
def pm(sort):
    sort.pm += 1

def degat(personnage, lanceur=None):
    personnage.pv -= 1
def ralentissement(personnage, lanceur=None):
    personnage.pm -= 1
def fatigue(personnage, lanceur=None):
    personnage.pa -= 1


class Etat:
    def __init__(self, *args):
        self.personnage = None
        self.lanceur = None
        self.conditions = [*args]
        
        self.duree = 1

    def run_conditions(self):
        for condition in self.conditions:
            condition(self)

    def fin_periode(self):
        """ Réduit d'un tour la durée. """
        self.duree -= 1
        if self.duree == 0:
            self.personnage.etats.remove(self)
            self.lanceur.etats_lances.remove(self)

    def duree(self):
        """ Permet de faire tenir l'état un tour de plus à partir du tour du personnage. """
        self.duree += 1

    def cible_sort(self, sort):
        """ Utilise l'état lorsque le joueur est touché par un sort. """
        pass


class Bouclier(Etat):
    def __init__(self, *args):
        Etat.__init__(self, *args)

        self.protection = 1

        self.run_conditions()
        print(self.duree)

    def protection(self):
        self.protection += 1

    def cible_sort(self, sort):
        protection = self.protection
        for application in list(sort.applications):
            if protection > 0 and application is degat:
                sort.applications.remove(application)
                protection -= 1


class Precision(Etat):
    def __init__(self, *args):
        Etat.__init__(self, *args)

        self.portee = 1

        self.run_conditions()

    def portee(self):
        self.portee += 1


def ajouter_etat(etat):
    def ajouter_etat(personnage, lanceur=None):
        personnage.etats.append(etat)
        etat.personnage = personnage
        lanceur.etats_lances.append(etat)
        etat.lanceur = lanceur
    return ajouter_etat

















