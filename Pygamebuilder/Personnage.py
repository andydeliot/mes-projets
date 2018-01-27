# coding=utf-8

from math import pi

import pygame
try:
    from Pygamebuilder.Game import Game
    from Pygamebuilder.Objet import Objet
    from Pygamebuilder.Texte import TexteObjet
    from Pygamebuilder.Arme import Arme
except ImportError:
    from Game import Game
    from Objet import Objet
    from Texte import TexteObjet
    from Arme import Arme

def nothing(self):
    pass


class Personnage(Objet):
    """ Les unités de base du jeu. """

    def __init__(self, x=Game.LARGEUR_ECRAN_METRE / 2, y=Game.HAUTEUR_ECRAN_METRE / 2, taille=1., vitesse=10,
                 vitesse_rotation=360, angle_vision=0,
                 nom_ia=nothing, nom="Heros", nom_equipe="allie", couleur=(0, 0, 255), priorite_affichage=80):
        Objet.__init__(self, x, y, taille, vitesse, vitesse_rotation, angle_vision, couleur, priorite_affichage)
        # Combat.
        self.vivant = True
        self.tempsMort = 0  # Définit depuis combien de temps l'unité est morte.
        self.pv_max = 100
        self.pv = self.pv_max
        # Arme.
        self.arme_primaire = Arme(self)
        self.arme_secondaire = Arme(self)
        self.equipements = []
        # Autre.
        self.vitesse_max = vitesse  # Metre par secondes. => pixel par image.
        self.vitesse_rotation_max = vitesse_rotation  # Angle en degré par secondes. => angle par image.

        # Ses forces sont utilisés afin de creer un poussement.
        self.forcePoussex = 0
        self.forcePoussey = 0

        # Variable gameplay.
        # En un cycle, une unité peut avancer et effectuer une rotation.
        self.cycle_deplacement = True
        self.cycle_rotation = True
        # Intelligence artificiel.
        self.nom_ia = nom_ia
        # Nom.
        self.nom = nom
        self.nom_equipe = nom_equipe

        self.texteNom = TexteObjet(self.x, self.y + self.taille + 2, self.nom)

        Game.personnages.append(self)

    def update(self):
        # Verifier que le personnage est vivant.
        self.vivant = True if self.pv > 0 else False
        # Mise à jour des cycles.
        self.cycle_deplacement = True
        self.cycle_rotation = True
        # Update.
        if self.vivant:
            self.executer_ia()
        self.actions_passives()

        # Update de l'objet normale.
        super().update()

    def afficher(self):
        # Nom du personnage.
        self.texteNom.x, self.texteNom.y = self.x, self.y - self.taille - (
            self.texteNom.taille / 2. / Game.PIXEL_PAR_METRE / Game.Vision.zoom)
        if self.vivant:
            # Cercle.
            self.dessiner_disque(self, self.taille, self.couleur)
            # Ligne de la direction de vision.
            xd, yd = Objet.position_graphique((self.x, self.y))
            xd2 = int((self.taille*1.6 * Game.PIXEL_PAR_METRE * Game.Vision.zoom) * Objet.cos(self.angle_vision * pi / 180.) + xd)
            yd2 = int((self.taille*1.6 * Game.PIXEL_PAR_METRE * Game.Vision.zoom) * Objet.sin(self.angle_vision * pi / 180.) + yd)
            pygame.draw.aaline(Game.Ecran, self.couleur, (xd, yd), (xd2, yd2))
            # Barre de vie.
            self.dessiner_barre(1, 50, self.pv, self.pv_max, (0, 255, 0))
            self.dessiner_barre(1.5, 50, self.pv, self.pv_max, (0, 255, 0))

            self.dessiner_barre(3, 50, self.arme_primaire.munitions, 10, (200, 200, 200))
            self.dessiner_barre(3.5, 50, self.arme_primaire.munitions, 10, (200, 200, 200))
        else:
            self.dessiner_cercle(self, self.taille, self.couleur)

    def calcul_degat(self, degat):
        protection = 0
        for equipement in self.equipements:
            protection += equipement.protection

        return degat * (1. - protection)

    def supprimer(self):
        Game.personnages.remove(self)
        self.texteNom.supprimer()
        super().supprimer()

    # Action passive.
    def passif_update_armes(self):
        self.arme_primaire.update()
        self.arme_secondaire.update()

    def passif_update_equipements(self):
        for equipement in self.equipements:
            equipement.update()

    def passif_force_de_pousse(self):
        self.x += self.forcePoussex
        self.y += self.forcePoussey
        self.forcePoussex *= 0.9
        self.forcePoussey *= 0.9

    def actions_passives(self):
        """ Active les actions passives. """
        # Vision.
        self.angle_vision = Objet.normaliser_angle(self.angle_vision)
        # Temps derniers coup tiré.
        self.passif_update_armes()
        # Equipement.
        self.passif_update_equipements()
        # Poussé.
        self.passif_force_de_pousse()
        # Se décaler.
        soldats = []
        for soldat in soldats:
            if soldat is not self:
                self.decaler(soldat)
        # Respawn spawner.
        if not self.vivant:
            self.tempsMort += Game.PERIODE

    def executer_ia(self):
        """ Intelligence artificiel à définir içi. """
        self.nom_ia(self)

    # Procédure.
    def utiliser_arme(self):
        """ Utilise l'arme portée actuellement.
        Pour changer d'arme, utlisé self.prendre_arme(nom_arme)
        """
        self.arme_primaire.utiliser()

    def utiliser_arme_sur(self, objet):
        """ Utilise l'arme portée actuellement sur l'objet visé.
        Pour changer d'arme, utlisé self.prendre_arme(nom_arme)
        :param objet: objet sur lequel utilisé l'arme.
        """
        self.arme_primaire.utiliser_sur(objet)

    def avancer(self):
        """ Avance le soldat dans la direction de sa vision. """
        if self.cycle_deplacement:
            Objet.avancer(self)
            self.cycle_deplacement = False

    def deplacement_droit(self):
        """ Déplace le soldat vers la droite de sa vision, en pas chassé.
            Le soldat est alors 2 fois plus lent. """
        if self.cycle_deplacement:
            super(Personnage, self).se_deplacer(self.angle_vision + 90, self.vitesse / 1.5)
            self.cycle_deplacement = False

    def deplacement_gauche(self):
        """ Déplace le soldat vers la gauche de sa vision, en pas chassé.
            Le soldat est alors 2 fois plus lent. """
        if self.cycle_deplacement:
            super(Personnage, self).se_deplacer(self.angle_vision - 90, self.vitesse / 1.5)
            self.cycle_deplacement = False

    def reculer(self):
        """ Déplace le soldat dans la direction inverse de sa vision.
            Le soldat est alors plus lent. """
        if self.cycle_deplacement:
            super(Personnage, self).se_deplacer(self.angle_vision - 180, self.vitesse / 2.)
            self.cycle_deplacement = False

    # 1,5 secondes pour faire un tour complet. 360/1.5 = 240, soit 2.4 degré par image.
    def pivoter_droit(self):
        """ Permet au soldat de pivoter dans le sens d'une aiguille d'une montre. """
        if self.cycle_rotation:
            super(Personnage, self).pivoter_droit()
            self.cycle_rotation = False

    def pivoter_gauche(self):
        """ Permet au soldat de pivoter dans le sens contraire d'une aiguille d'une montre. """
        if self.cycle_rotation:
            super(Personnage, self).pivoter_gauche()
            self.cycle_rotation = False

    def orienter_vers(self, objet, angle=0):
        """ Permet d'orienter le soldat vers une direction (50°), un point (x,y) ou un Objet.
            Exemple pour tourner le dos a un objet: self.OrienterVers(unObjet,180).
            :param objet: une direction (50°), un point (x,y) ou un Objet vers lequel s'orienter.
            :param angle: un nombre en degré permettant au soldat de dévié son orientation.
            """
        if self.cycle_rotation:
            super(Personnage, self).orienter_vers(objet, angle)
            self.cycle_rotation = False

    def positionner_devant(self, objet, angle, metre):
        """ Permet de positionner le soldat a une certaine distance d'un Objet à une position précise.
        :param objet: un Objet ou une position (x,y) vers lequel se positionner.
        :param angle: un angle en degré. Celui ci permet de placer le soldat à une certaine position de différence.
        :param metre: une distance en metre. Cette distance permettra de placer l'objet à la distance de diff à l'objet.
        Exemple: PositionerDevant(commandant,commandant.AngleVision()+90,5) :
        Permet de positionner le soldat a 5 metre du commandant à 90 degré de sa direction de vision.
        Cette fonction permet entre autre de creer des formations.
        """
        self.avancer_vers(self.position_devant(objet, angle, metre))

    # Procédures ajoutées le 26/11/2015 (auteur : Tehema) #
    def decaler(self, objet):  # non fini
        """ Décale le soldat par rapport à l'objet
        Attention, on attend que les deux objets soient en collision
                => il faut faire un test si les 2 objets sont en collision avant l'appel à cette procédure
        C'est l'instance courante qui se décale (décalage le plus court)
        :param objet: objet avec lequel se décaler.
        """
        if self.collision(objet):
            dz = self.get_taille() + objet.get_taille() - self.distance_avec(objet)
            dx = dz * self.cos(self.angle_avec(objet))
            dy = dz * self.sin(self.angle_avec(objet))
            self.x -= dx
            self.y -= dy
        else:
            pass

    # Donnée.
    def get_vivant(self):
        """ Retourne True si le soldat est vivant, False s'il est mort. """
        if self.vivant:
            return True
        else:
            return False

    def get_temps_mort(self):
        """ Retourne le temps en secondes depuis lequel le personnage est mort. """
        return self.tempsMort

    @staticmethod
    def trouver_personnage_par_nom(nom):
        personnages = [personnage for personnage in Game.personnages if personnage.nom == nom]
        return personnages

    @staticmethod
    def personnages_equipe(nom_equipe):
        personnages = [personnage for personnage in Game.personnages if personnage.nom_equipe == nom_equipe]
        return personnages

    def __repr__(self):
        return "Personnage " + self.nom
