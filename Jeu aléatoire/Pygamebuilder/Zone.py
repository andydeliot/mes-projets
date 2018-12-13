
class Spawner(Objet):
    def __init__(self, x, y, rayon, cooldownRespawn=20):
        joueur = ""  # Le spawner n'as pas besoin de joueur. C'est le joueur qui a besoin du spawner.
        Objet.__init__(self, joueur, x, y)
        self.rayon = rayon  # Metre.
        self.cooldownRespawn = cooldownRespawn  # Secondes.

    def Update(self):
        self.PriseBase()

    def CreerSoldat(self, univers, joueur):
        while True:
            x = randint(int(self.x - self.rayon), int(self.x + self.rayon))
            y = randint(int(self.y - self.rayon), int(self.y + self.rayon))
            obj = Objet("", x, y)
            if self.ObjetDansBase(obj): break
        univers.CreerSoldat(joueur, x, y)

    def ObjetDansBase(self, objet):
        """ Return True si l'Objet objet est dans la base.
            False sinon."""
        if self.Distance(objet) <= self.rayon:
            return True
        else:
            return False

    def PriseBase(self, objets):
        """ Return True si un ou plusieurs Objet dans la liste objets sont dans la base.
            False sinon."""
        for obj in objets:
            if self.ObjetDansBase(obj):
                return True
        return False


##    def PriseBase(self):
##        """ Regarde si un soldat ennemi est dans la zone de prise de la base. """
##        soldatPreneur = ""
##        for soldat in self.joueur.univers.soldats:
##            if soldat.vivant:
##                if self.ObjetDansBase(soldat):
##                    if soldatPreneur != "":
##                        if soldatPreneur.joueur != soldat.joueur:
##                            soldatPreneur = ""
##                            break
##                    else:
##                        soldatPreneur = soldat
##
##        if soldatPreneur != "":
##            if soldatPreneur.joueur != self.joueur:
##                # Changement d'appartenance.
##                self.joueur.spawners.remove(self)
##                self.joueur = soldatPreneur.joueur
##                self.joueur.spawners.append(self)
