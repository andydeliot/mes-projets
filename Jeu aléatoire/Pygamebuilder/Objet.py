    # coding=utf-8

from math import pi, sin, cos, acos, asin

import pygame
from pygame import gfxdraw

try:
    from Pygamebuilder.Game import Game
except:
    from Game import Game

class Objet:
    """ Représente tout les objets du jeu. """

    def __init__(self, x=2, y=2, taille=2, vitesse=10, vitesse_rotation=360, angle_vision=0, couleur=(0, 255, 0), priorite_affichage=20):

        self.x, self.y = x, y  # Position absolut en metre.
        self.taille = taille  # rayon de l'objet en metre.
        self.vitesse = vitesse  # Metre par secondes.
        self.vitesse_rotation = vitesse_rotation  # Angle en degré par secondes.
        self.angle_vision = angle_vision  # angle degré normalisé. (voir la fonction normaliser_angle(angle))

        self.couleur = couleur
        self.priorite_affichage = priorite_affichage

        Game.objets.append(self)

    # Donnée.
    def type(self):
        """ Retourne le type de l'objet en lettre. (ex pour un soldat leger: retourne "SoldatLeger"). """
        return self.__class__.__name__

    def get_angle_vision(self):
        """ Retourne la direction en degré de l'angle directif de l'objet.
            Entre -180 et 180 : le 0 se trouvant a droite, le 90 en bas, le 180 et -180 a gauche, et le -90 en haut. """
        return self.angle_vision

    def set_angle_vision(self, angle):
        """
        :param angle: un angle normalisé ou non.
        :return: Modifie la valeur de angleVision de l'objet.
        """
        self.angle_vision = Objet.normaliser_angle(angle)

    def get_x(self):
        """ Retourne la position x de l'objet en metre.
            Le 0 est a gauche, le 250 tout a droite."""
        return self.x

    def get_y(self):
        """ Retourne la position y de l'objet en metre.
            Le 0 est en haut, le 250 tout en bas."""
        return self.y

    def get_taille(self):
        """
        :return: Retourne la taille de l'objet.
        """
        return self.taille

    def get_vitesse(self):
        """
        :return: Retourne la vitesse max de l'objet en metre par secondes.
        """
        return self.vitesse

    def get_vitesse_rotation(self):
        """
        :return: Retourne la vitesse de rotation maximum en degré par secondes.
        """
        return self.vitesse_rotation

    def position(self):
        """ Retourne la position de l'objet en metre (x,y).
        Si x est grand, l'objet est vers la droite.
        Si y est grand, l'objet est vers le bas.
        """
        x = self.get_x()
        y = self.get_y()
        return x, y

    # Fonction d'information.
    def objet_le_plus_proche(self, objets):
        """ Recherche l'objet le plus proche de soi dans la liste objets.
            Retourne l'objet si celui ci est trouvé.
            Retourne '' (une chaine vide) si aucun objet n'as été trouvé (cela signifie que la liste 'objets' est vide).
            :param objets: liste d'objets dans lequel la fonction va chercher l'objet le plus proche.
                            Si self est contenue dans objets, il n'est pas comptabilisé.
            """
        objet_proche = ""
        distance_min = 1000000
        for objet in objets:
            if objet is not self:
                dx = abs(objet.get_x() - self.get_x())
                dy = abs(objet.get_y() - self.get_y())
                d = (dx ** 2 + dy ** 2) ** 0.5
                if d < distance_min:
                    objet_proche = objet
                    distance_min = d
        return objet_proche

    def distance_avec(self, objet):
        """ Donne la distance entre les deux objets en metre.
            Retourne un nombre en metre.
            objet peut etre un Objet ou une position (x,y) en metre
            :param objet: un Objet. """
        if objet != "":
            if isinstance(objet, Objet):
                x, y = objet.position()
            else:
                x, y = objet
            dx = (x - self.get_x())
            dy = (y - self.get_y())
            dz = self.taille_hypothenuse(dx, dy)
            return dz
        else:
            return ""

    def touche_position(self, position):
        """ Renvoi vrai si la position touche l'objet. """
        return self.distance_avec(position) < self.taille

    def est_clique(self):
        """ Renvoi vrai si l'objet est cliqué. """
        if not Game.clic_gauche() and not Game.clic_droit():
            return False
        return self.touche_position(self.position_logique(Game.position_souris()))
            

    # Fonctions ajoutées le 26/11/2015 (auteur : Tehema) #
    def collision_avec(self, objet):
        """ Vérifie si deux objets sont en collisions
        A partir de la distance entre les deux objets et leur taille
        Retourne un booléen (True or False)
        :param objet: Un objet.
            """
        if isinstance(objet, Objet):
            return self.distance_avec(objet) < self.get_taille() + objet.get_taille()
        else:
            return self.distance_avec(objet) < self.get_taille()

    def angle_avec(self, objet):
        """ Donne l'angle entre deux objet en degré.
        Retourne un nombre en degré (entre -180 et 180).
        Le 0 se trouve a droite, 90 en bas, 180 ou -180 a gauche, -90 en haut.
        :param objet: un Objet ou une position (x,y) en metre.
        """
        if isinstance(objet, Objet):
            x, y = objet.position()
        else:
            x, y = objet
        dx = (x - self.get_x())
        dy = (y - self.get_y())
        dz = (dx ** 2 + dy ** 2) ** 0.5
        try:
            rad = acos(dx / dz)
        except ZeroDivisionError:
            rad = 0
        angle = self.radian_en_degre(rad)
        if dy < 0:
            angle = - angle
        return angle

    @staticmethod
    def position_devant(objet, angle, metre):
        """ retourne une position définit par un point, la distance entre ce point et un angle en degré.
        :param objet: un Objet ou une position (x,y) vers lequel se positionner.
        :param angle: un angle en degré. Celui ci permet de placer le soldat à une certaine position de différence.
        :param metre: une distance en metre. Cette distance permettra de placer l'objet à la distance de diff à l'objet.
        :return la position (x, y) correspondant au calcule.
        """
        angle_radian = angle * pi / 180.
        x = cos(angle_radian) * metre
        y = sin(angle_radian) * metre
        if isinstance(objet, Objet):
            x += objet.get_x()
            y += objet.get_y()
        else:
            x += objet[0]
            y += objet[1]
        return x, y

    @staticmethod
    def normaliser_angle(angle):
        """ Transforme un angle en angle normalisé, c'est a dire, un angle entre 180 et -180 degré.
        :param angle: Ange en degré. Le 0 se trouve a droite, 90 en bas, 180 ou -180 a gauche, -90 en haut.
        """
        while angle <= -180:
            angle += 360
        while angle > 180:
            angle -= 360
        return angle

    @staticmethod
    def angle_en_pygame(angle):
        """ Retourne un angle en convention Pygame.
        C'est à dire, le 0 en haut, le 90 à gauche, et le -90 à droite.
        :param angle: angle en degré normalisé ou non.
        """
        return Objet.normaliser_angle(-angle - 90)

    @staticmethod
    def degre_en_radian(angle):
        """ Transforme un angle en degré en angle en radian.
        :param angle: un angle normalisé ou non en degré.
        """
        return Objet.normaliser_angle(angle) * pi / 180.

    @staticmethod
    def radian_en_degre(angle):
        """ Transforme un angle en radian en angle en degré.
        :param angle: Un angle normalisé ou non en radian.
        """
        return Objet.normaliser_angle(round(angle * 180. / pi, 5))  # Précision de 5 chiffres apres la virgules.

    @staticmethod
    def taille_hypothenuse(x, y):
        """ Renvoie la taille de l'hypothénuse d'un triangle (Le plus long coté d'un triangle).
        :param x: la taille d'un des deux coté du triangle rectangle.
        :param y: le coté opposé.
        """
        return ((x ** 2) + (y ** 2)) ** 0.5

    @staticmethod
    def taille_cote_oppose(z, angle):
        """ Renvoie la taille du coté opposé de l'angle.
        :param z: la taille de l'hypothénuse.
        :param angle: angle en degré.
        """
        rad = Objet.degre_en_radian(angle)
        return z * sin(rad)

    @staticmethod
    def taille_cote_adjacent(z, angle):
        """ Renvoie la taille du coté adjacent de l'angle.
        :param z: la taille de l'hypothénuse.
        :param angle: un angle en degré.
        """
        rad = Objet.degre_en_radian(angle)
        return z * cos(rad)

    @staticmethod
    def cos(rad):
        """ Renvoie le cosinus de l'angle en radian.
        :param rad: angle en radian.
        """
        return cos(rad)

    @staticmethod
    def sin(rad):
        """ Renvoie le sinus de l'angle en radian.
        :param rad: angle en radian.
        """
        return sin(rad)

    @staticmethod
    def arc_cos(cosinus):
        """ Renvoie l'arc cosinus d'un cosinus.
        :param cosinus: Cosinus.
        """
        return acos(cosinus)

    @staticmethod
    def arc_sin(sinus):
        """ Renvoie l'arc sinus d'un sinus.
        :param sinus: Sinus.
        """
        return asin(sinus)

    @staticmethod
    def difference_angle(angle1, angle2):
        """ Donne la différence entre les deux angles en degré.
        Retourne un nombre en degré (entre 0 et 180).
        :param angle1: angle en degré normalisé ou non.
        :param angle2: angle en degré normalisé ou non.
        """
        dangle = abs(angle1 - angle2)
        dangle = Objet.normaliser_angle(dangle)
        dangle = abs(dangle)
        return dangle

    @staticmethod
    def difference_angle_non_absolut(angle1, angle2):
        """ Donne la différence entre deux angles en degré. (angle1 - angle2)
        angle1 et angle2 sont deux nombres représentant des angles en degré.
        Retourne un nombre en degré (entre -180 et 180).
        :param angle1: angle en degré normalisé ou non.
        :param angle2: angle en degré normalisé ou non."""
        dangle = angle1 - angle2
        dangle = Objet.normaliser_angle(dangle)
        return dangle

    @staticmethod
    def exclure_liste(liste1, liste2):
        """ Permet de soustraire liste2 a liste1.
        :param liste1: Une liste d'objets à laquelle on va enlever des éléments avec liste2.
        :param liste2: listes d'objets à enlever de la premiere liste.
        """
        for a in liste2:
            i = 0
            while i < len(liste1):
                if liste1[i] is a:
                    liste1.remove(a)
                else:
                    i += 1
        return liste1

    @staticmethod
    def unir_liste(liste1, liste2):
        """ Permet d'additionner les liste afin de donner une liste ayant tout les éléments des deux listes.
        Supprime les doublons.
        Retourne une liste.
        :param liste1: Une liste à unir.
        :param liste2: Une autre liste à unir. """
        liste = []
        for a in liste1:
            liste.append(a)
        for b in liste2:
            if b not in liste:
                liste.append(b)
        return liste

    # Action.
    def supprimer(self):
        Game.objets.remove(self)

    def se_deplacer(self, angle, vitesse):
        """ Avance l'objet par angle.
        :param angle: angle normalisé ou non.
        :param vitesse: vitesse à laquelle l'objet va se déplacer.
        """
        angle_radian = Objet.normaliser_angle(angle) * pi / 180.
        vx = cos(angle_radian) * vitesse * Game.PERIODE
        vy = sin(angle_radian) * vitesse * Game.PERIODE
        self.x += vx
        self.y += vy

    def avancer(self):
        """
        :return: L'objet est avancé dans la direction de sa Game.Vision.
        """
        self.se_deplacer(self.angle_vision, self.vitesse)

    def avancer_vers(self, objet, angle=0):
        """ Déplace l'objet vers un objet ou une position.
            :param objet: un Objet ou une position (x,y) en metre.
            :param angle: un nombre en degré permettant au soldat de dévié de sa trajectoire.
            """
        if objet != "":
            if self.distance_avec(objet) > (self.taille/10.):
                self.orienter_vers(objet, angle)
                # Avancer.
                self.avancer()

    def pivoter_droit(self):
        """ Permet a l'objet de pivoter dans le sens d'une aiguille d'une montre. """
        self.angle_vision += self.vitesse_rotation * Game.PERIODE

    def pivoter_gauche(self):
        """ Permet a l'objet de pivoter dans le sens contraire d'une aiguille d'une montre. """
        self.angle_vision -= self.vitesse_rotation * Game.PERIODE

    def orienter_vers(self, objet, angle=0):
        """ Permet d'orienter l'objet vers une direction (50°), un point (x,y) ou un autre Objet.
        :param objet: un Objet, une direction (50°) ou un point (x,y).
        :param angle: nombre en degré permettant au soldat de dévié son orientation.
        """
        pos = ""
        if isinstance(objet, Objet):
            pos = objet.position()
        elif type(objet) is tuple or type(objet) is list:
            pos = objet

        degre = angle
        if type(pos) is tuple or type(pos) is list:
            angle = self.angle_avec(pos)
        if type(objet) is int or type(objet) is float:
            angle = objet
        angle += degre

        angle = Objet.normaliser_angle(angle)
        dd = Objet.difference_angle_non_absolut(angle, self.angle_vision)

        if dd > (self.vitesse_rotation * Game.PERIODE):
            self.pivoter_droit()
        elif dd < -(self.vitesse_rotation * Game.PERIODE):
            self.pivoter_gauche()
        else:
            self.angle_vision = angle

    # Graphisme
    def update(self):
        self.afficher()

    def afficher(self):
        """ Affiche l'objet a l'écran. """
        Objet.dessiner_disque(self, self.taille, self.couleur)
        # Objet.dessiner_cercle(self, self.taille, self.couleur)

    def get_couleur(self):
        """ Retourne la couleur en (R, V, B) du Game.Vision a qui appartient l'objet.
        """
        return self.couleur

    @staticmethod
    def position_graphique(point):
        """ Définit la position graphique d'un point en prenant en compte 3 paramètres. :
                La Game.Vision du Game.Vision,le centre de l'écran, et le zoom.
        :param point: une position [x,y] en mètre correspondant au point du jeu.
        :return (xd, yd) qui sont des points en pixels représentant la position final des points sur l'écran.
        """
        dx = point[0] * Game.PIXEL_PAR_METRE
        dy = point[1] * Game.PIXEL_PAR_METRE
        dx = (dx + Game.Vision.visionx) - Game.CENTREX
        dy = (dy + Game.Vision.visiony) - Game.CENTREY
        dx *= (Game.Vision.zoom - 1.)
        dy *= (Game.Vision.zoom - 1.)
        xd = int(point[0] * Game.PIXEL_PAR_METRE + Game.Vision.visionx + dx)
        yd = int(point[1] * Game.PIXEL_PAR_METRE + Game.Vision.visiony + dy)
        return xd, yd

    @staticmethod
    def position_logique(point):
        """ Définit la position logique d'un point en prenant en compte 3 paramètres. :
                La Game.Vision du Game.Vision,le centre de l'écran, et le zoom.
        :param point: une position [x,y] en pixels correspondant au point sur l'écran.
        :return (x, y) qui sont des points en mètre représentant la position final des points dans le jeu.
        """
        x = (-Game.Vision.visionx + Game.CENTREX + (point[0] - Game.CENTREX) / Game.Vision.zoom) / Game.PIXEL_PAR_METRE
        y = (-Game.Vision.visiony + Game.CENTREY + (point[1] - Game.CENTREY) / Game.Vision.zoom) / Game.PIXEL_PAR_METRE
        return x, y

    @staticmethod
    def dessiner_disque(objet, rayon, couleur):
        """ Dessine un cercle rempli sur le terrain.
        :param objet: Objet ou position (x,y) en metre permettant de définir la position du disque sur le terrain.
        :param rayon: le rayon du disque en metre.
        :param couleur: (R,V,B) avec Rouge, Vert et Bleu entre 0 et 255 ex: Blanc = (0,0,0), Noir = (255,255,255)
        """
        pos = ""
        if isinstance(objet, Objet):
            pos = objet.position()
        elif type(objet) is tuple or type(objet) is list:
            pos = objet

        xd, yd = Objet.position_graphique(pos)
        rayond = int(rayon * Game.PIXEL_PAR_METRE * Game.Vision.zoom)
        rayond = 2 if rayond < 2 else rayond

        try:
            pygame.gfxdraw.filled_circle(Game.Ecran, xd, yd, int(rayond), couleur)
        except OverflowError:
            pass

    @staticmethod
    def dessiner_cercle(objet, rayon, couleur):
        """ Dessine un cercle sur le terrain.
        :param objet: Objet ou position (x,y) en metre permettant de définir la position du disque sur le terrain.
        :param rayon: le rayon du disque en metre.
        :param couleur: (R,V,B) avec Rouge, Vert et Bleu entre 0 et 255 ex: Blanc = (0,0,0), Noir = (255,255,255)
        """
        pos = ""
        if isinstance(objet, Objet):
            pos = objet.position()
        elif type(objet) is tuple or type(objet) is list:
            pos = objet

        xd, yd = Objet.position_graphique(pos)
        rayond = int(rayon * Game.PIXEL_PAR_METRE * Game.Vision.zoom)
        rayond = 2 if rayond < 2 else rayond

        try:
            pygame.gfxdraw.aacircle(Game.Ecran, xd, yd, int(rayond), couleur)
        except OverflowError:
            pass

    @staticmethod
    def dessiner_rectangle(objet, largeur, hauteur, couleur):
        pos = ""
        if isinstance(objet, Objet):
            pos = objet.position()
        elif type(objet) is tuple or type(objet) is list:
            pos = objet

        xd, yd = Objet.position_graphique(pos)
        largeurd = largeur  # int(largeur * Game.PIXEL_PAR_METRE * Game.Vision.zoom)
        hauteurd = hauteur  # int(hauteur * Game.PIXEL_PAR_METRE * Game.Vision.zoom)
        largeurd = 2 if largeurd < 2 else largeurd
        hauteurd = 2 if hauteurd < 2 else hauteurd

        try:
            pygame.draw.polygon(Game.Ecran, couleur,
                                [[xd - largeurd, yd - hauteurd], [xd + largeurd, yd - hauteurd],
                                 [xd + largeurd, yd + hauteurd], [xd - largeurd, yd + hauteurd]])
        except OverflowError:
            pass

    @staticmethod
    def dessiner_ligne(objet1, objet2, couleur):
        """ Dessine une ligne sur le terrain.
        :param objet1: Objet ou position (x,y) en metre. Il permet de définir le point de départ de la ligne.
        :param objet2: Objet ou position (x,y) en metre. Il permet de définir le point d'arrivé de la ligne.
        :param couleur: (R,V,B) avec Rouge, Vert et Bleu entre 0 et 255 ex: Blanc = (0,0,0), Noir = (255,255,255)
        """
        pos1 = ""
        if isinstance(objet1, Objet):
            pos1 = objet1.position()
        elif type(objet1) is tuple or type(objet1) is list:
            pos1 = objet1
        pos2 = ""
        if isinstance(objet2, Objet):
            pos2 = objet2.position()
        elif type(objet2) is tuple or type(objet2) is list:
            pos2 = objet2

        xd, yd = Objet.position_graphique(pos1)
        xd2, yd2 = Objet.position_graphique(pos2)
        try:
            pygame.draw.aaline(Game.Ecran, couleur, (xd, yd), (xd2, yd2))
        except OverflowError:
            pass

    def dessiner_barre(self, position, taille_bar, variable, variable_max, couleur):
        """ Dessine une barre tel une barre de vie.
        :param position: Numéro de position de la barre. C'est un entier.
        :param taille_bar: Taille de la barre si la variable est égale à la variable maximum.
                La taille de la barre est égale a tailleBar * variable / variableMax (sans compter le zoom).
        :param variable: Designe la variable a tester.
        :param variable_max: Designe la valeur maximal de la variable a tester.
        :param couleur: (R,V,B) avec Rouge, Vert et Bleu entre 0 et 255 ex: Blanc = (0,0,0), Noir = (255,255,255)
        """
        if type(variable) is not str and type(variable_max) is not str:
            if variable > 0 and variable_max > 0:
                taille_bar = int(taille_bar * Game.Vision.zoom)

                xd, yd = Objet.position_graphique((self.x, self.y))

                tailled = int(self.taille * Game.PIXEL_PAR_METRE * Game.Vision.zoom)
                if tailled < 2:
                    tailled = 2

                pygame.gfxdraw.hline(Game.Ecran, int(xd - taille_bar / 2),
                                     int(xd - taille_bar / 2 + (taille_bar * float(variable) / float(variable_max))),
                                     int(yd + tailled + (position * 3)), couleur)
                pygame.gfxdraw.hline(Game.Ecran, int(xd - taille_bar / 2),
                                     int(xd - taille_bar / 2 + (taille_bar * float(variable) / float(variable_max))),
                                     int(yd + tailled + (position * 3) + 1), couleur)

    def __repr__(self):
        return str(self.__class__.__name__) + " en " + str(self.x) + ", " + str(self.y)
