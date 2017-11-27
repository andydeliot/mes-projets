import os
import pytest
from fourmizzzing import *

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




























if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
















