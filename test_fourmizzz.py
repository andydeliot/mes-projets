import os
import pytest
from combazzz import *

# Setup.

@pytest.fixture()
def troupe1():
    return Troupe(jsn, 1000)


def test_troupe():
    troupe = Troupe(jsn, 1000)
    assert troupe.vie == 8000
    assert troupe.attaque == 3000
    assert troupe.defense == 2000
    assert troupe.nourriture == 16000
    assert troupe.__repr__() == "Jeune soldate naine(1000)"

    assert troupe.egale(Troupe(jsn, 1000))
    assert not troupe.egale(Troupe(jsn, 999))
    assert not troupe.egale(Troupe(s, 1000))

def test_armee():
    armee = Armee(Troupe(jsn, 1000), Troupe(s, 500))
    assert armee.vie == 18000
    assert armee.attaque == 10500
    assert armee.defense == 9000
    assert armee.nourriture == 34000

    assert armee.egale(Armee(Troupe(jsn, 1000), Troupe(s, 500)))
    assert not armee.egale(Armee(Troupe(jsn, 999), Troupe(s, 500)))
    assert not armee.egale(Armee(Troupe(jsn, 1000), Troupe(se, 500)))


def test_attaquer():
    armee1 = Armee(Troupe(jsn, 1000))
    armee2 = Armee().attaquer(armee1, 4000)
    assert armee2.vie == 4000
    assert armee2.troupes[0].nombre == 500

def test_combattre():
    armee1 = Armee(Troupe(jsn, 1000))
    armee2 = Armee(Troupe(jsn, 1000))
    armee3, armee4 = armee1.combattre(armee2)
    assert armee3.__repr__() == "[Jeune soldate naine(493)]"

def test_difference():
    armee1 = Armee(Troupe(jsn, 1000), Troupe(s, 500))
    armee2 = Armee(Troupe(jsn, 800), Troupe(s, 400))
    armee3 = armee1.difference(armee2)
    assert armee3.egale(Armee(Troupe(jsn, 200), Troupe(s, 100)))
    assert not armee3.egale(Armee(Troupe(jsn, 100), Troupe(s, 100)))
    assert not armee3.egale(Armee(Troupe(jsn, 200), Troupe(se, 100)))

def test_operateur():
    armee1 = Armee(Troupe(jsn, 1000))
    assert armee1 == Armee(Troupe(jsn, 1000))
    assert armee1 < Armee(Troupe(jsn, 1010))
    assert Armee(Troupe(c, 1000)) == Armee(Troupe(c, 1000))

    assert armee1 > Armee(Troupe(jsn, 500))
    assert armee1 < Armee(Troupe(jsn, 1500))











































if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
















