# coding=latin-1
from unittest import TestCase

from Objet import *


class TestObjet(TestCase):
    # -*- coding: latin-1 -*-

    def setUp(self):
        self.monObjet = Objet(5, 10, 2, 3, 90)

    def tearDown(self):
        self.monObjet = None

    def test_Type(self):
        self.assertEquals(self.monObjet.type(), "Objet")

    def test_AngleVision(self):
        self.assertLess(self.monObjet.get_angle_vision(), 180)
        self.assertGreater(self.monObjet.get_angle_vision(), -180)

    def test_X(self):
        self.assertEquals(self.monObjet.get_x(), 5)

    def test_Y(self):
        self.assertEquals(self.monObjet.get_y(), 10)

    def test_Position(self):
        self.assertEquals(self.monObjet.position(), (5, 10))

    def test_ObjetLePlusProche(self):
        obj1 = Objet(8, 10)
        obj2 = Objet(7, 10)
        self.assertEquals(self.monObjet.objet_le_plus_proche([obj1, obj2]), obj2)

    def test_ObjetLePlusProcheListeVide(self):
        self.assertEquals(self.monObjet.objet_le_plus_proche([]), "")

    def test_Distance(self):
        self.assertEquals(self.monObjet.distance_avec(Objet(8, 14)), 5)

    def test_DistanceZero(self):
        self.assertEquals(self.monObjet.distance_avec(self.monObjet), 0)

    def test_NormaliserAngleNormale(self):
        self.assertEquals(Objet.normaliser_angle(130), 130)

    def test_NormaliserAngle180(self):
        self.assertEquals(Objet.normaliser_angle(180), 180)

    def test_NormaliserAngleNegatif(self):
        self.assertEquals(Objet.normaliser_angle(-130), -130)

    def test_NormaliserAngleMoins180(self):
        self.assertEquals(Objet.normaliser_angle(-180), 180)

    def test_NormaliserAngleTropGrand(self):
        self.assertEquals(Objet.normaliser_angle(190), -170)

    def test_NormaliserAngleTropPetit(self):
        self.assertEquals(Objet.normaliser_angle(-190), 170)

    def test_NormaliserAngleSuperPetit(self):
        self.assertEquals(Objet.normaliser_angle(-1440), 0)

    def test_AngleRadian(self):
        self.assertEquals(Objet.degre_en_radian(90), pi / 2)

    def test_AngleRadianNull(self):
        self.assertEquals(Objet.degre_en_radian(0), 0)

    def test_AngleRadian360(self):
        self.assertEquals(Objet.degre_en_radian(360), 0)

    def test_AngleRadianSuperGrand(self):
        self.assertEquals(Objet.degre_en_radian(1440), 0)

    def test_AngleDegre(self):
        self.assertEquals(Objet.radian_en_degre(pi), 180)

    def test_AngleDegreNull(self):
        self.assertEquals(Objet.radian_en_degre(0), 0)

    def test_AngleDegre3Pi(self):
        self.assertEquals(Objet.radian_en_degre(3 * pi), 180)

    def test_TailleHypothenuse(self):
        self.assertEquals(Objet.taille_hypothenuse(3, 4), 5)

    def test_TailleHypothenuseNombreNegatif(self):
        self.assertEquals(Objet.taille_hypothenuse(-3, -4), 5)

    def test_TailleCoteOppose(self):
        self.assertAlmostEquals(Objet.taille_cote_oppose(50, 45), 35.3553390593)

    def test_TailleCoteOpposeNombreNegatif(self):
        self.assertAlmostEquals(Objet.taille_cote_oppose(50, 45), 35.3553390593)

    def test_TailleCoteAdjacent(self):
        self.assertAlmostEquals(Objet.taille_cote_adjacent(50, 45), 35.3553390593)

    def test_TailleCoteAdjacentNombreNegatif(self):
        self.assertAlmostEquals(Objet.taille_cote_adjacent(50, 45), 35.3553390593)

    def test_CosPiSur2(self):
        self.assertAlmostEquals(Objet.cos(pi / 2), 0)

    def test_CosPiSur3(self):
        self.assertAlmostEquals(Objet.cos(pi / 3), 0.5)

    def test_SinPiSur2(self):
        self.assertAlmostEquals(Objet.sin(pi / 2), 1)

    def test_SinPiSur3(self):
        self.assertAlmostEquals(Objet.sin(pi / 3), 0.8660254038)

    def test_ArcCos(self):
        self.assertAlmostEquals(Objet.arc_cos(0.5), pi / 3)

    def test_ArcSin(self):
        self.assertAlmostEquals(Objet.arc_sin(0.8660254038), pi / 3)

    def test_ExclusionListe(self):
        liste1 = [1, 2, 3, 4]
        liste2 = [1, 4]
        liste = Objet.exclure_liste(liste1, liste2)
        self.assertEquals(liste, [2, 3])

    def test_ExclusionListeVide(self):
        liste1 = []
        liste2 = [1, 4]
        liste = Objet.exclure_liste(liste1, liste2)
        self.assertEquals(liste, [])

    def test_ExclusionListeElementDifferent(self):
        liste1 = [1, 2, 3, 4]
        liste2 = [6, 5]
        liste = Objet.exclure_liste(liste1, liste2)
        self.assertEquals(liste, [1, 2, 3, 4])

    def test_ExclusionListePlusieursMemeElement(self):
        liste1 = [1, 2, 3, 4, 4, 4, 4]
        liste2 = [1, 4]
        liste = Objet.exclure_liste(liste1, liste2)
        self.assertEquals(liste, [2, 3])

    def test_UnionListe(self):
        liste1 = [1, 2]
        liste2 = [3, 4]
        liste = Objet.unir_liste(liste1, liste2)
        self.assertEquals(liste, [1, 2, 3, 4])

    def test_UnionListeVide(self):
        liste1 = [1, 2]
        liste2 = []
        liste = Objet.unir_liste(liste1, liste2)
        self.assertEquals(liste, [1, 2])

    def test_UnionListePlusieursMemeElement(self):
        liste1 = [1, 2]
        liste2 = [1, 2]
        liste = Objet.unir_liste(liste1, liste2)
        self.assertEquals(liste, [1, 2])

    # Tests ajoutés le 26/11/2015 (auteur : Tehema) #
    def test_AngleObjBasDroit(self):
        """test si obj2 est en bas a droite d'obj1"""
        obj1 = Objet(10, 10)
        obj2 = Objet(40, 40)
        self.assertEquals(obj1.angle_avec(obj2), 45)

    def test_AngleObjBasGauche(self):
        """test si obj2 est en bas a gauche d'obj1"""
        obj1 = Objet(40, 10)
        obj2 = Objet(10, 40)
        self.assertEquals(obj1.angle_avec(obj2), 135)

    def test_AngleObjHautDroit(self):
        """test si obj2 est en haut a droite d'obj1"""
        obj1 = Objet(10, 40)
        obj2 = Objet(40, 10)
        self.assertEquals(obj1.angle_avec(obj2), -45)

    def test_AngleObjHautGauche(self):
        """test si obj2 est en haut a gauche d'obj1"""
        obj1 = Objet(40, 40)
        obj2 = Objet(10, 10)
        self.assertEquals(obj1.angle_avec(obj2), -135)

    def test_Avancer(self):
        self.monObjet.set_angle_vision(90)
        for a in range(Game.HERTZ):
            self.monObjet.avancer()
        self.assertAlmostEquals(self.monObjet.get_x(), 5)
        self.assertAlmostEquals(self.monObjet.get_y(), 13)

    # Tests ajoutés le 26/11/2015 (auteur : Tehema) #
    def test_Collision(self):
        sld1 = Objet(10, 10, 5, 0, 0)
        sld2 = Objet(15, 10, 5, 0, 0)
        self.assertTrue(sld1.collision_avec(sld2))

    def test_PasDeCollision(self):
        # class Soldat(joueur,x,y,santeMax,taille,vitesseMax,vitesseRotationMax,armes)
        sld1 = Objet(10, 10, 5, 0, 0)
        sld2 = Objet(20, 10, 5, 0, 0)
        self.assertFalse(sld1.collision_avec(sld2))

    def test_PositionGraphiqueZoom1(self):
        xd, yd = Objet.position_graphique((200, 200), (0, 0), (500, 500), 1)
        self.assertEquals((xd, yd), (200, 200))

    def test_PositionGraphiqueZoom2(self):
        xd, yd = Objet.position_graphique((200, 200), (0, 0), (500, 500), 2)
        self.assertEquals((xd, yd), (-100, -100))

    def test_PositionGraphiqueZoom05(self):
        xd, yd = Objet.position_graphique((200, 200), (0, 0), (500, 500), 0.5)
        self.assertEquals((xd, yd), (350, 350))

    def test_PositionGraphiqueVisionXY50(self):
        xd, yd = Objet.position_graphique((200, 200), (50, 50), (500, 500), 1)
        self.assertEquals((xd, yd), (250, 250))

    def test_PositionGraphiqueVisionXY50Zoom2(self):
        xd, yd = Objet.position_graphique((200, 200), (50, 50), (500, 500), 2)
        self.assertEquals((xd, yd), (0, 0))

    def test_PositionGraphiquePositionNegative(self):
        xd, yd = Objet.position_graphique((-500, -500), (0, 0), (500, 500), 3)
        self.assertEquals((xd, yd), (-2500, -2500))

    def test_PositionGraphiquePositionSurCentre(self):
        xd, yd = Objet.position_graphique((500, 500), (0, 0), (500, 500), 10)
        self.assertEquals((xd, yd), (500, 500))

    def test_PositionGraphiqueVisionXY50Zoom05(self):
        xd, yd = Objet.position_graphique((200, 200), (50, 50), (500, 500), 0.5)
        self.assertEquals((xd, yd), (375, 375))

    def test_NormaliserAnglePygame0Degre(self):
        """ Le zero se trouve normalement à droite. Avec Pygame, il se trouve en haut. """
        self.assertEquals(Objet.angle_en_pygame(0), -90)

    def test_NormaliserAnglePygame90Degre(self):
        """ Normalement, on tourne dans le sens d'une aiguille d'une montre.
            Avec Pygame, c'est le sens inverse. """
        self.assertEquals(Objet.angle_en_pygame(90), 180)

    def test_NormaliserAnglePygameMoins90Degre(self):
        """ Le -90 se trouve normalement en haut. Avec Pygame, il se trouve a gauche. """
        self.assertEquals(Objet.angle_en_pygame(-90), 0)

    def test_NormaliserAnglePygame180Degre(self):
        """ Le 180 se trouve normalement à gauche. Avec Pygame, il se trouve en bas. """
        self.assertEquals(Objet.angle_en_pygame(180), 90)


if __name__ == "__main__":
    TestObjet()
