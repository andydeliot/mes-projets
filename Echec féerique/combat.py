
from pygame import gfxdraw
from pygame import Surface
from pygame import Rect



def distance_echequier(case1, case2):
    """ Retourne la distance à parcourir pour se trouver de la case1 à la case2. """
    return abs(case1.x - case2.x) + abs(case1.y - case2.y)



class Case:
    def __init__(self, x, y):
        self.x, self.y = x, y
        
        self.taille = 70
        posx = self.x * Terrain.TAILLE_CASE
        posy = self.y * Terrain.TAILLE_CASE
        self.rect = Rect(posx, posy, self.taille, self.taille)

    def update(self, surface):
        couleur = (255, 255, 255) if (self.x + self.y) % 2 else (0, 0, 0)
        surface.fill(couleur, self.rect)
        gfxdraw.rectangle(surface, self.rect, couleur)

    def update_portee(self, surface):
        surface.fill((0, 0, 75), self.rect)
        gfxdraw.rectangle(surface, self.rect, (0, 0, 150))

    def update_selection(self, surface):
        surface.fill((75, 0, 0), self.rect)
        gfxdraw.rectangle(surface, self.rect, (150, 0, 0))

    def __eq__(self, other):
        if type(other) is Case:
            return True if self.x == other.x and self.y == other.y else False
        else:
            return False

    def __repr__(self):
        return "Case [{0},{1}]".format(self.x, self.y)


class Terrain:
    TAILLE_CASE = 70
    def __init__(self, taillex, tailley, Ecran):
        self.cases = []
        for y in range(tailley):
            ligne = []
            for x in range(taillex):
                ligne.append(Case(x, y))
            self.cases.append(ligne)

        self.personnages = []
        self.personnage_actif = None
        self.num_joueur = -1

        self.case_selectionnees = []

    def update(self, Ecran):
        surface = Surface(Ecran.get_size())
        # Cases.
        for ligne in self.cases:
            for case in ligne:
                if case in self.case_selectionnees:
                    case.update_selection(surface)
                elif self.personnage_actif.sort is not None:
                    if self.personnage_actif.sort.check_conditions(case, self):
                        case.update_portee(surface)
                    else:
                        case.update(surface)
                else:
                    case.update(surface)
        # Personnages.
        for personnage in self.personnages:
            personnage.update(surface)
        # Affichage.
        Ecran.blit(surface, (0, 0))

    def clic_case(self, pos):
        for ligne in self.cases:
            for case in ligne:
                if case.rect.collidepoint(pos):
                    return case

    def ajouter_personnage(self, *personnages):
        for personnage in personnages:
            self.personnages.append(personnage)

    def run(self):
        assert len(self.personnages) > 0, "Aucun joueur dans la partie"

        if self.personnage_actif is not None:
            self.personnage_actif.run()

    def personnage_suivant(self):
        self.personnage_actif = self.personnages[self.num_joueur]
        self.personnage_actif.activer_etats("fin du tour")
        self.personnage_actif.personnage_suivant()
        
        self.num_joueur += 1
        if self.num_joueur >= len(self.personnages):
            self.num_joueur = 0
        self.personnage_actif = self.personnages[self.num_joueur]
        self.personnage_actif.activer_etats("début du tour")

    def zonage(self, case, portee, portee_minimum):
        cases = []
        for ligne in self.cases:
            for case2 in ligne:
                if (distance_echequier(case, case2) <= portee and
                    distance_echequier(case, case2) >= portee_minimum):
                    cases.append(case2)
        return cases


class Personnage:
    def __init__(self, couleur, x, y, pv=50, pa=6, pm=3, ini=100):
        self.couleur = couleur
        self.x, self.y = x, y
        self.taille = 70 # Graphique.
        
        self.pv = pv
        self.pa_max, self.pa = pa, pa
        self.pm_max, self.pm = pm, pm
        self.ini = ini

        self.sorts = []
        self.sort = None

        self.etats = []

    def update(self, Ecran):
        posx = self.x * Terrain.TAILLE_CASE + int(self.taille/2)
        posy = self.y * Terrain.TAILLE_CASE + int(self.taille/2)
        gfxdraw.filled_circle(Ecran, posx, posy, int(self.taille/2), self.couleur)

    def run(self):
        pass

    def get_case(self):
        return Case(self.x, self.y)

    def personnage_suivant(self):
        self.pa = self.pa_max
        self.pm = self.pm_max
        self.sort = None

    def deplacement_gauche(self):
        if self.pm > 0:
            self.pm -= 1
            self.x -= 1
    def deplacement_droite(self):
        if self.pm > 0:
            self.pm -= 1
            self.x += 1
    def deplacement_haut(self):
        if self.pm > 0:
            self.pm -= 1
            self.y -= 1
    def deplacement_bas(self):
        if self.pm > 0:
            self.pm -= 1
            self.y += 1

    def activer_etats(self, activation):
        for etat in self.etats:
            etat.run(activation)

    def __repr__(self):
        return "{0} pv, {1} pa, {2} pm".format(self.pv,self.pa,self.pm)


class Sort:
    def __init__(self, personnage, conditions=[], applications=[]):
        self.personnage = personnage
        self.personnage.sorts.append(self)
        
        self.conditions = conditions
        self.portee = 0
        self.portee_minimum = 0
        self.zone = 0
        self.zone_minimum = 0
        self.pa = 0
        self.pm = 0
        self.pv = 0
        for condition in self.conditions:
            condition(self)
        assert self.portee >= self.portee_minimum, "Portée < à portée minimum"
        assert self.zone >= self.zone_minimum, "Zone < à zone minimum"

        self.applications = applications

    def run(self, case, terrain):
        if self.run_conditions(case, terrain):
            cases = terrain.zonage(case, self.zone, self.zone_minimum)
            for case2 in cases:
                for personnage in terrain.personnages:
                    if personnage.get_case() == case2:
                        applications_personnage = list(self.applications)
                        for etat in personnage.etats:
                            applications_personnage = etat.run("cible d'un sort", applications_personnage)
                        for application in applications_personnage:
                            application(personnage)

    def run_conditions(self, case, terrain):
        if self.check_conditions(case,terrain):
            self.personnage.pa -= self.pa
            self.personnage.pm -= self.pm
            self.personnage.pv -= self.pv
            return True
        return False

    def check_conditions(self, case, terrain):
        distance = distance_echequier(case, self.personnage.get_case())
        if distance > self.portee:
            return False
        if distance < self.portee_minimum:
            return False
        if self.pa > self.personnage.pa:
            return False
        if self.pm > self.personnage.pm:
            return False
        return True


# Conditions
def pa(sort):
    sort.pa += 1
def pm(sort):
    sort.pm += 1
def pv(sort):
    sort.pv += 1
def portee(sort):
    sort.portee += 1
def portee_minimum(sort):
    sort.portee_minimum += 1
def zone(sort):
    sort.zone += 1
def zone_minimum(sort):
    sort.zone_minimum += 1
# Conditions états
def duree(etat):
    etat.duree += 1

# Applications
def degat(personnage):
    personnage.pv -= 1

def fatigue(personnage):
    personnage.pa -= 1

def energie(personnage):
    personnage.pa += 1

def ralentissement(personnage):
    personnage.pm -= 1

def vitesse(personnage):
    personnage.pm += 1

def ajouter_etat(etat):
    def ajouter_etat(personnage):
        personnage.etats.append(etat(personnage))
    return ajouter_etat





class Etat:
    def __init__(self, personnage, activation, conditions=[]):
        self.personnage = personnage
        self.activation = activation

        self.conditions = conditions
        self.duree = 1

        for condition in self.conditions:
            condition(self)

def poison(conditions=[]):
    class Poison(Etat):
        def __init__(self, personnage):
            Etat.__init__(self, personnage, "fin du tour", conditions)

        def run(self, activation, applications=[]):
            if activation == self.activation:
                degat(self.personnage)
                self.duree -= 1
                if self.duree == 0:
                    self.personnage.etats.remove(self)
    return Poison


def bouclier(conditions=[]):
    class Bouclier(Etat):
        def __init__(self, personnage):
            Etat.__init__(self, personnage, "cible d'un sort", conditions)

        def run(self, activation, applications=[]):
            if activation == self.activation:
                new_applications = []
                resistance = 1
                for application in applications:
                    if application is not degat or resistance == 0:
                        new_applications.append(application)
                    else:
                        resistance -= 1
                return new_applications

    return Bouclier












































        
