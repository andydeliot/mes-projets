import os
import pytest
from combazzz import *

# Setup.

@pytest.fixture()
def fourmilliere():
    return Fourmilliere(0, 0, 0, 0, 0)

@pytest.fixture()
def jsn():
    ma_fourmilliere = Fourmilliere(0, 0, 0, 0, 0)
    return JeuneSoldateNaine(ma_fourmilliere, 1, "Terrain de chasse")


# Fourmis.

def test_fourmis_1_degat(jsn):
    jsn.subir(7)
    assert jsn.vie == 1
    assert jsn.nombre == 1

def test_2_fourmis_9_degat(jsn, fourmilliere):
    jsn = JeuneSoldateNaine(fourmilliere, 2)
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

def test_fourmilliere_attaque():
    f1 = Fourmilliere()
    jsn1 = JeuneSoldateNaine(f1, 1)
    f2 = Fourmilliere()
    jsn2 = JeuneSoldateNaine(f2, 1)
    f1.attaquer(f2, "Terrain de chasse", jsn1)
    assert f2.armees.__repr__() == "[]"
    assert f1.armees.__repr__() == "[Jeune soldate naine (1)]"
    assert jsn1.vie == 8

def test_fourmilliere_attaque_perdu():
    f1 = Fourmilliere()
    jsn1 = JeuneSoldateNaine(f1, 1)
    f2 = Fourmilliere()
    jsn2 = JeuneSoldateNaine(f2, 4)
    f1.attaquer(f2, "Terrain de chasse", jsn1)
    assert f1.armees.__repr__() == "[]"
    assert f2.armees.__repr__() == "[Jeune soldate naine (4)]"
    assert jsn2.vie == 32




##@pytest.fixture()
##def troupe1():
##    return Troupe(jsn, 1000)
##
##
##def test_troupe():
##    troupe = Troupe(jsn, 1000)
##    assert troupe.vie == 8000
##    assert troupe.attaque == 3000
##    assert troupe.defense == 2000
##    assert troupe.nourriture == 16000
##    assert troupe.__repr__() == "Jeune soldate naine(1000)"
##
##    assert troupe.egale(Troupe(jsn, 1000))
##    assert not troupe.egale(Troupe(jsn, 999))
##    assert not troupe.egale(Troupe(s, 1000))
##
##def test_subi():
##    troupe = Troupe(jsn, 1000)
##    troupe = troupe.subi(4000)
##    assert troupe.vie == 4000
##    assert troupe.nombre == 500
##    assert Troupe(jsn, 1).subi(50).nombre == 0
##
##
##def test_armee():
##    armee = Armee(Troupe(jsn, 1000), Troupe(s, 500))
##    assert armee.vie == 18000
##    assert armee.attaque == 10500
##    assert armee.defense == 9000
##    assert armee.nourriture == 34000
##
##    assert armee.egale(Armee(Troupe(jsn, 1000), Troupe(s, 500)))
##    assert not armee.egale(Armee(Troupe(jsn, 999), Troupe(s, 500)))
##    assert not armee.egale(Armee(Troupe(jsn, 1000), Troupe(se, 500)))
##
##def test_attaquer():
##    armee1 = Armee(Troupe(jsn, 1000))
##    armee2 = Armee().attaquer(armee1, 4000)
##    assert armee2.vie == 4000
##    assert armee2.troupes[0].nombre == 500
##
##def test_combattre():
##    armee1 = Armee(Troupe(jsn, 1000))
##    armee2 = Armee(Troupe(jsn, 1000))
##    armee3, armee4 = armee1.combattre(armee2)
##    assert armee3.__repr__() == "[Jeune soldate naine(493)]"
##    assert (Armee(Troupe(jsn, 1)).combattre(Armee(Troupe(jsn, 1)))).__repr__() == "([Jeune soldate naine(1)], [])"
##
##def test_difference():
##    armee1 = Armee(Troupe(jsn, 1000), Troupe(s, 500))
##    armee2 = Armee(Troupe(jsn, 800), Troupe(s, 400))
##    armee3 = armee1.difference(armee2)
##    assert armee3.egale(Armee(Troupe(jsn, 200), Troupe(s, 100)))
##    assert not armee3.egale(Armee(Troupe(jsn, 100), Troupe(s, 100)))
##    assert not armee3.egale(Armee(Troupe(jsn, 200), Troupe(se, 100)))
##
##def test_operateur():
##    armee1 = Armee(Troupe(jsn, 1000))
##    assert armee1 == Armee(Troupe(jsn, 1000))
##    assert armee1 < Armee(Troupe(jsn, 1010))
##    assert Armee(Troupe(c, 1000)) == Armee(Troupe(c, 1000))
##
##    assert armee1 > Armee(Troupe(jsn, 500))
##    assert armee1 < Armee(Troupe(jsn, 1500))
##
##
##








































if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
















