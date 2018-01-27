import os
import pytest
from fourmizzzing import *
from datetime import timedelta

# Setup.

@pytest.fixture()
def f():
    return Fourmilliere()



def test_creation_fourmilliere(f):
    assert f.browser.url == "http://s4.fourmizzz.fr/Ressources.php"

def test_connexion(f):
    f.connexion()
    assert f.browser.url == "http://s4.fourmizzz.fr/Reine.php"

def test_page(f):
    f.page("Reine")
    assert f.browser.url == "http://s4.fourmizzz.fr/Reine.php"
    f.page("Ressources")
    assert f.browser.url == "http://s4.fourmizzz.fr/Ressources.php"
    f.page("Construction")
    assert f.browser.url == "http://s4.fourmizzz.fr/construction.php"
    f.page("Laboratoire")
    assert f.browser.url == "http://s4.fourmizzz.fr/laboratoire.php"
    f.page("Armée")
    assert f.browser.url == "http://s4.fourmizzz.fr/Armee.php"

def test_get_ressource(f):
    f.page("Reine")
    f.get_ressource()
    assert f.browser.url == "http://s4.fourmizzz.fr/Reine.php"
    f.page("Ressources")
    f.get_ressource()
    assert f.browser.url == "http://s4.fourmizzz.fr/Ressources.php"
    f.page("Construction")
    f.get_ressource()
    assert f.browser.url == "http://s4.fourmizzz.fr/construction.php"
    f.page("Laboratoire")
    f.get_ressource()
    assert f.browser.url == "http://s4.fourmizzz.fr/laboratoire.php"
    f.page("Armée")
    f.get_ressource()
    assert f.browser.url == "http://s4.fourmizzz.fr/Armee.php"

    assert f.ouvrieres != 0
    assert f.nourriture != 0
    assert f.bois != 0
    assert f.tdc != 0

def test_get_armee(f):
    f.get_armee()
    assert f.browser.url == "http://s4.fourmizzz.fr/Armee.php"
    assert f.armee != {}

def test_get_temps_chasse(f):
    f.get_temps_chasse()
    assert f.browser.url == "http://s4.fourmizzz.fr/Ressources.php"

def test_faire_travailler(f):
    f.faire_travailler()
    assert f.browser.url == "http://s4.fourmizzz.fr/Ressources.php"


def test_parser_temps():
    assert parser_temps("1s") == timedelta(seconds=1)
    assert parser_temps("36s") == timedelta(seconds=36)
    assert parser_temps("0.80s") == timedelta(seconds=0.8)
    assert parser_temps("1.72s") == timedelta(seconds=1.72)
    assert parser_temps("5.99s") == timedelta(seconds=5.99)

    assert parser_temps("25m 51s") == timedelta(minutes=25, seconds=51)
    assert parser_temps("59m") == timedelta(minutes=59)
    assert parser_temps("14h 39m 10s") == timedelta(hours=14, minutes=39, seconds=10)
    assert parser_temps("22h") == timedelta(hours=22)
    assert parser_temps("3j 7h 47m 55s") == timedelta(days=3, hours=7, minutes=47, seconds=55)
    assert parser_temps("15j") == timedelta(days=15)

























if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
















