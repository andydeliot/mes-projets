# coding=utf-8


## Univers ##
class Univers:
    """ La classe qui gère toutes les classes. """

    def __init__(self):
        self.objet = Objet("", 0, 0)  # Afin d'utiliser les fonctions à partir de l'univers.

        self.CreationJoueur()

        # Objets et terrain.
        self.temps = 0
        self.dureeCombat = 900

        self.CreationEquipe()
        shuffle(VariableGlobale.soldats)  # Mélange la liste des soldats. Pour ne pas qu'il y est de priorité d'attaque.

    # Joueurs.
    def CreerJoueur(self, nom, x, y, rayonSpawner):
        """ Creer un joueur avec son nom, et son spawner avec sa position x,y et son rayon.
            Le joueur est automatiquement rajouté à la map.
            le joueur est automatiquement lié à l'univers. (joueur.univers = self)"""
        spawner = Spawner(x, y, rayonSpawner)
        joueur = Joueur(nom, spawner)
        joueur.univers = self
        VariableGlobale.joueurs.append(joueur)

    def CreationJoueur(self):
        """ Creer les joueurs sur la map. Les spawners respecte une distance minimal entre eux. """
        tailleSpawner = 1  # metre.
        distanceMinimalSpawner = 8
        while True:
            VariableGlobale.joueurs = []
            for a in range(VariableGlobale.NB_JOUEURS):
                x = randint(tailleSpawner, VariableGlobale.TAILLE_TERRAIN - tailleSpawner)
                y = randint(tailleSpawner, VariableGlobale.TAILLE_TERRAIN - tailleSpawner)
                self.CreerJoueur("joueur{0}".format(a + 1), x, y, tailleSpawner)
            if self.DistanceMinimalSpawner(distanceMinimalSpawner): break

    def DistanceMinimalSpawner(self, distanceMinimal):
        """ Observe si la distance minimal entre les spawners sont respecté.
            Return True si la distance minimal est respecté.
            False sinon."""
        distanceRespecte = True
        for j1 in VariableGlobale.joueurs:
            for j2 in VariableGlobale.joueurs:
                if j1 is not j2:
                    self.objet.get_x = j1.spawner.get_x
                    self.objet.get_y = j1.spawner.get_y
                    if self.objet.distance_avec(j2.spawner) < distanceMinimal:
                        distanceRespecte = False
        return distanceRespecte

    def CreationEquipe(self, nbrSoldat=5):
        """ Creer l'équipe des joueurs avec un nombre de nbrSoldat soldats."""
        for joueur in VariableGlobale.joueurs:
            for b in range(nbrSoldat):
                joueur.spawner.CreerSoldat(self, joueur)

    def CreerSoldat(self, joueur, x, y):
        """ Mais que peut faire une fonction nommé CreerSoldat ?...
            Bah ... ça creer un soldat.
            Le soldat est lié au joueur. (soldat.joueur = joueur)"""
        soldat = Guerrier(joueur, x, y)
        soldat.get_x = x
        soldat.get_y = y
        VariableGlobale.soldats.append(soldat)
        joueur.nbrSoldat -= 1

    # Soldats.
    def CollisionSoldatProjectile(self, soldat, projectile):
        """ Returne True si le soldat et le projectile sont en collision.
            False sinon.
            Prend en compte la taille du soldat et de la balle."""
        if soldat.distance_avec(projectile) < soldat.taille + projectile.taille:
            return True
        else:
            return False

    def DeclanchementCollisionSoldatProjectile(self, soldat, projectile):
        projectile.collision_avec(soldat)
        soldat.arme.chargementCoup = 0
        self.ApplicationDegat(soldat)

    def CollisionProjectile(self, soldat):
        """ Regarde si le soldat c'est fait toucher par une balle et applique les dégats. """
        for balle in list(VariableGlobale.projectiles):
            if self.CollisionSoldatProjectile(soldat, balle):
                balle.collision_avec(soldat)
                soldat.arme.chargementCoup = 0
        self.ApplicationDegat(soldat)

    def ApplicationDegat(self, soldat):
        """ Applique les dégats sur le soldat. """
        if soldat.sante < 0 and soldat.vivant:
            soldat.vivant = False
            soldat.tempsMort = 0

    def Update(self):

        # Update.
        for projectile in list(VariableGlobale.projectiles):
            projectile.first_update()

        for soldat in list(VariableGlobale.soldats):
            self.CollisionProjectile(soldat)
            soldat.first_update()

            # Blocage mur.
            tailleSoldat = soldat.taille
            if soldat.get_x + tailleSoldat > VariableGlobale.TAILLE_TERRAIN: soldat.get_x = VariableGlobale.TAILLE_TERRAIN - tailleSoldat
            if soldat.get_x - tailleSoldat < 0: soldat.get_x = tailleSoldat
            if soldat.get_y + tailleSoldat > VariableGlobale.TAILLE_TERRAIN: soldat.get_y = VariableGlobale.TAILLE_TERRAIN - tailleSoldat
            if soldat.get_y - tailleSoldat < 0: soldat.get_y = tailleSoldat

            # Ressurection.
            if soldat.tempsMort > 5 and soldat.get_joueur.nbrSoldat > 0:
                VariableGlobale.soldats.remove(soldat)
                soldat.get_joueur.spawner.CreerSoldat(self, soldat.get_joueur)

        # Incrémentation temps.
        self.temps += VariableGlobale.HERTZ
