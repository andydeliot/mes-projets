import os
import pytest
from combazzz import *

# Setup.

@pytest.fixture()
def jsn():
    return JeuneSoldateNaine(Fourmilliere(), 1, "Terrain de chasse")


# Fourmis.

def test_fourmis():
    f1 = Fourmilliere()

    with pytest.raises(AssertionError):
        Soldate("Une fourmilliere", 1)
    with pytest.raises(AssertionError):
        Soldate(f1, -1)
    with pytest.raises(AssertionError):
        Soldate(f1, 1.5)
    with pytest.raises(AssertionError):
        Soldate(f1, 1, "Terrain non existant")

    Soldate(f1, 1)
    assert f1.armees.__repr__() == "[Soldate (1)]"
    Soldate(f1, 1, "Dome")
    assert f1.armees.__repr__() == "[Soldate (1), Soldate (1)]"
    Soldate(f1, 1, "Loge")
    assert f1.armees.__repr__() == "[Soldate (1), Soldate (1), Soldate (1)]"

def test_fourmis_1_degat(jsn):
    jsn.subir(7)
    assert jsn.vie == 1
    assert jsn.nombre == 1

def test_2_fourmis_9_degat(jsn):
    jsn = JeuneSoldateNaine(Fourmilliere(), 2)
    jsn.subir(9)
    assert jsn.vie == 7
    assert jsn.nombre == 1

def test_fourmis_100_degat(jsn):
    jsn.subir(100)
    assert jsn.vie == 0
    assert jsn.nombre == 0

def test_fourmis_degat_negatif(jsn):
    with pytest.raises(AssertionError):
        jsn.subir(-1)
    assert jsn.vie == 8
    assert jsn.nombre == 1

def test_fourmis_bonus_50():
    jsn = JeuneSoldateNaine(Fourmilliere(dome=8), 1, "Dome")
    jsn.subir(11)
    assert jsn.vie == 1
    assert jsn.nombre == 1


def test_fourmis_point_attaque(jsn):
    assert jsn.point_attaque() == 3

def test_fourmis_point_attaque_bonus_1():
    jsn = JeuneSoldateNaine(Fourmilliere(arme=1), 1)
    assert jsn.point_attaque() == 3

def test_fourmis_point_attaque_bonus_2():
    jsn = JeuneSoldateNaine(Fourmilliere(arme=2), 1)
    assert jsn.point_attaque() == 4

def test_10_fourmis_point_attaque_bonus_1():
    jsn = JeuneSoldateNaine(Fourmilliere(arme=1), 10)
    assert jsn.point_attaque() == 33


def test_fourmis_point_defense(jsn):
    assert jsn.point_defense() == 2

def test_fourmis_point_defense_bonus_1():
    jsn = JeuneSoldateNaine(Fourmilliere(defense=1), 1)
    assert jsn.point_defense() == 2

def test_fourmis_point_defense_bonus_2():
    jsn = JeuneSoldateNaine(Fourmilliere(defense=2), 1)
    assert jsn.point_defense() == 2

def test_10_fourmis_point_defense_bonus_1():
    jsn = JeuneSoldateNaine(Fourmilliere(defense=1), 10)
    assert jsn.point_defense() == 22


# Fourmilliere.

def test_fourmilliere_combattre():
    f1 = Fourmilliere()
    jsn1 = JeuneSoldateNaine(f1, 1)
    f2 = Fourmilliere()
    jsn2 = JeuneSoldateNaine(f2, 1)
    f1.combattre(f2, "Terrain de chasse", jsn1)
    assert f2.armees.__repr__() == "[]"
    assert f1.armees.__repr__() == "[Jeune soldate naine (1)]"
    assert jsn1.vie == 8

def test_fourmilliere_combat_perdu():
    f1 = Fourmilliere()
    jsn1 = JeuneSoldateNaine(f1, 1)
    f2 = Fourmilliere()
    jsn2 = JeuneSoldateNaine(f2, 4)
    f1.combattre(f2, "Terrain de chasse", jsn1)
    assert f1.armees.__repr__() == "[]"
    assert f2.armees.__repr__() == "[Jeune soldate naine (4)]"
    assert jsn2.vie == 32

def test_fourmilliere_combat_emplacement_non_existant():
    with pytest.raises(AssertionError):
        Fourmilliere().combattre(Fourmilliere(), "Terrain non existant")


def test_fourmilliere_attaque_loge():
    f1 = Fourmilliere()
    jsn1 = JeuneSoldateNaine(f1, 4)
    f2 = Fourmilliere()
    jsn2 = JeuneSoldateNaine(f2, 1)
    jsn3 = JeuneSoldateNaine(f2, 1, "Loge")
    f1.attaquer(f2, "Loge", jsn1)
    assert jsn1.vie == 32
    assert jsn1.nombre == 4
    assert jsn2.vie == 0
    assert jsn2.nombre == 0
    assert jsn3.vie == 0
    assert jsn3.nombre == 0

def test_fourmilliere_attaque_emplacement_non_existant():
    with pytest.raises(AssertionError):
        Fourmilliere().attaquer(Fourmilliere(), "Terrain non existant")


def test_fourmilliere_copie():
    f1 = Fourmilliere()
    Soldate(f1, 1)
    f2 = f1.copier()
    assert f1 is not f2
    assert f1.armees[0] is not f2.armees[0]
    assert f1.armees[0].fourmilliere is f1
    assert f2.armees[0].fourmilliere is f2












































if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
















