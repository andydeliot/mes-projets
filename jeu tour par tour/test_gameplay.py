# coding: utf-8


import os
import pytest

from gameplay import *


# Fonctions

def test_distance_echiquier():
    assert distance_echequier(Case(0, 0), Case(0, 0)) == 0
    assert distance_echequier(Case(0, 1), Case(0, 1)) == 0
    assert distance_echequier(Case(1, 0), Case(1, 0)) == 0
    assert distance_echequier(Case(0, 0), Case(0, 1)) == 1
    assert distance_echequier(Case(1, 0), Case(0, 0)) == 1
    assert distance_echequier(Case(1, 1), Case(0, 0)) == 2
    assert distance_echequier(Case(5, 6), Case(7, 8)) == 4

# Fixtures

@pytest.fixture()
def terrain():
    return Terrain(10, 10)

@pytest.fixture()
def p1(terrain):
    return Personnage(terrain, "Héros", x=5, y=5)

@pytest.fixture()
def p2(terrain):
    return Personnage(terrain, "Méchant", x=6, y=5)

@pytest.fixture()
def s1(p1):
    s1 = Sort(p1,
              conditions=[portee, pa, pm],
              applications=[degat, ralentissement, fatigue])
    return s1

@pytest.fixture()
def s2(p2):
    s2 = Sort(p2,
              conditions=[portee, pa, pa, pa, pm, pm],
              applications=[degat, degat, degat])
    return s2

@pytest.fixture()
def s_zone(p1):
    s_zone = Sort(p1,
              conditions=[portee, portee, zone, pa, pm],
              applications=[degat, degat, degat])
    return s_zone

@pytest.fixture()
def s_bouclier(p1):
    etat_bouclier = Bouclier(Bouclier.protection,
                             Bouclier.duree, Bouclier.duree)
    s_bouclier = Sort(p1,
                      conditions=[],
                      applications=[ajouter_etat(etat_bouclier)])
    return s_bouclier

@pytest.fixture()
def s_precision(p1):
    etat_precision = Precision(Precision.portee,
                               Precision.duree, Precision.duree, Precision.duree)
    s_precision = Sort(p1,
                       conditions=[],
                       applications=[ajouter_etat(etat_precision)])
    return s_precision


# Terrain

def test_terrain():
    t = Terrain(10, 10)
    assert len(t.cases) == 100
    assert t.personnages == []

def test_tour_par_tour(terrain, p1, p2):
    assert terrain.personnage_actif is None
    terrain.start()
    assert terrain.personnage_actif is p1
    terrain.fin_de_tour()
    assert terrain.personnage_actif is p2
    terrain.fin_de_tour()
    assert terrain.personnage_actif is p1

def test_tour_par_tour_regain_pa_et_pm(terrain, p1):
    terrain.start()
    assert terrain.personnage_actif is p1
    assert p1.pa == 6
    assert p1.pm == 3
    p1.pa = 0
    p1.pm = 0
    terrain.fin_de_tour()
    assert p1.pa == 6
    assert p1.pm == 3

# Personnage

def test_personnage(terrain):
    p = Personnage(terrain, nom="Héros", x=5, y=5)
    assert len(terrain.personnages) == 1
    assert terrain.personnages[0] is p
    assert p.pv == 50
    assert p.pa == 6
    assert p.pm == 3
    assert str(p) == "Personnage Héros en (5, 5) 50 pv, 6 pa, 3 pm"
    assert p.sorts == []
    assert p.selection_sort == None
    assert p.etats == []

def test_personnage_deplacement(p1):
    assert p1.x == 5
    assert p1.y == 5
    p1.pm == 4
    p1.deplacement_haut()
    assert p1.x == 5
    assert p1.y == 4
    p1.deplacement_droite()
    assert p1.x == 6
    assert p1.y == 4
    p1.deplacement_bas()
    assert p1.x == 6
    assert p1.y == 5
    p1.deplacement_gauche()
    assert p1.x == 5
    assert p1.y == 5

def test_personnage_deplacement_perte_pm(p1):
    p1.pm = 4
    assert p1.pm == 4
    p1.deplacement_haut()
    assert p1.pm == 3
    p1.deplacement_bas()
    assert p1.pm == 2
    p1.deplacement_droite()
    assert p1.pm == 1
    p1.deplacement_gauche()
    assert p1.pm == 0

def test_personnage_deplacement_bord_de_terrain(p1):
    p1.y = 0
    p1.deplacement_haut()
    assert p1.x == 5
    assert p1.y == 0
    
    p1.y = 9
    p1.deplacement_bas()
    assert p1.x == 5
    assert p1.y == 9

    p1.y = 5

    p1.x = 0
    p1.deplacement_gauche()
    assert p1.x == 0

    p1.x = 9
    p1.deplacement_droite()
    assert p1.x == 9

    p1.x = 5

def test_personnage_deplacement_bloque_par_personnage2(p1, p2):
    assert p2.x == p1.x + 1
    assert p2.y == p1.y
    p1.deplacement_droite()
    assert p2.x == p1.x + 1
    assert p2.y == p1.y
    p2.deplacement_gauche()
    assert p2.x == p1.x + 1
    assert p2.y == p1.y
    p2.x = p1.x
    p2.y = p1.y+1
    p1.deplacement_bas()
    assert p2.x == p1.x
    assert p2.y == p1.y + 1
    p2.deplacement_haut()
    assert p2.x == p1.x
    assert p2.y == p1.y + 1
    

# Sort.

def test_sort(p1):
    assert p1.selection_sort is None
    s1 = Sort(p1,
              conditions=[portee, pa, pm],
              applications=[degat, ralentissement, fatigue])
    assert p1.selection_sort is s1
    assert len(p1.sorts) == 1
    assert p1.sorts[0] is s1
    p1.selectionner_sort()
    assert p1.selection_sort is s1
    p1.selectionner_sort(numero=0)
    assert p1.selection_sort is s1
    with pytest.raises(IndexError):
        p1.selectionner_sort(numero=1)

def test_lancer_sort1_case_vide(p1, s1):
    p1.selectionner_sort()
    assert p1.pa == 6
    assert p1.pm == 3
    p1.lancer_sort(4, 5)
    assert p1.pa == 5
    assert p1.pm == 2
    p1.lancer_sort(4, 5)
    assert p1.pa == 4
    assert p1.pm == 1
    
    p1.pa = 0
    p1.pm = 3
    p1.lancer_sort(4, 5)
    assert p1.pa == 0
    assert p1.pm == 3
    p1.pa = 6
    p1.pm = 0
    p1.lancer_sort(4, 5)
    assert p1.pa == 6
    assert p1.pm == 0

def test_lancer_sort1_trop_loin(p1, s1):
    assert s1.portee == 1
    p1.selectionner_sort()
    p1.pa = 6
    p1.pm = 3
    p1.lancer_sort(1, 1)
    assert p1.pa == 6
    assert p1.pm == 3

def test_lancer_sort1_p2(p1, s1, p2):
    p1.selectionner_sort()
    assert p2.pv == 50
    p1.lancer_sort(6, 5)
    assert p2.pv == 49

def test_lancer_sort2_case_vide(p2, s2):
    p2.selectionner_sort()
    assert p2.pa == 6
    assert p2.pm == 3
    p2.lancer_sort(7, 5)
    assert p2.pa == 3
    assert p2.pm == 1

def test_lancer_sort2_p1(p2, s2, p1):
    p2.selectionner_sort()
    assert p1.pv == 50
    p2.lancer_sort(5, 5)
    assert p1.pv == 47

def test_lancer_sort_zone_case_vide(p1, s_zone):
    p1.selectionner_sort()
    assert p1.x, p1.y == (5, 5)
    assert p1.pv == 50
    assert p1.pa == 6
    assert p1.pm == 3
    p1.lancer_sort(3, 5)
    assert p1.pv == 50
    assert p1.pa == 5
    assert p1.pm == 2

def test_lancer_sort_zone_soi_meme(p1, s_zone):
    p1.selectionner_sort()
    assert p1.x, p1.y == (5, 5)
    assert p1.pv == 50
    assert p1.pa == 6
    assert p1.pm == 3
    p1.lancer_sort(4, 5)
    assert p1.pv == 47
    assert p1.pa == 5
    assert p1.pm == 2
    p1.lancer_sort(5, 5)
    assert p1.pv == 44
    assert p1.pa == 4
    assert p1.pm == 1

def test_lancer_sort_zone_p2(p1, s_zone, p2):
    p1.selectionner_sort()
    assert p2.x, p2.y == (6, 5)
    assert p2.pv == 50
    assert p1.x, p1.y == (5, 5)
    assert p1.pv == 50
    p1.lancer_sort(6, 6)
    assert p2.pv == 47
    assert p1.pv == 50
    p1.lancer_sort(6, 5)
    assert p2.pv == 44
    assert p1.pv == 47
    assert p1.pa == 4
    assert p1.pm == 1


# Etat

def test_duree_bouclier(p1):
    etat_bouclier = Bouclier(Bouclier.protection, Bouclier.protection,
                             Bouclier.duree, Bouclier.duree)
    s_bouclier = Sort(p1,
                      conditions=[],
                      applications=[ajouter_etat(etat_bouclier)])
    assert len(p1.etats) == 0
    p1.lancer_sort(5, 5)
    assert p1.etats[0] == etat_bouclier
    p1.fin_de_tour()
    assert p1.etats[0] == etat_bouclier
    
    p1.debut_de_tour()
    assert p1.etats[0] == etat_bouclier
    p1.fin_de_tour()
    assert p1.etats[0] == etat_bouclier

    p1.debut_de_tour()
    assert p1.etats[0] == etat_bouclier
    p1.fin_de_tour()
    assert p1.etats[0] == etat_bouclier

    p1.debut_de_tour()
    assert len(p1.etats) == 0

def test_duree_bouclier_avec_terrain(terrain, p1):
    etat_bouclier = Bouclier(Bouclier.protection,
                             Bouclier.duree, Bouclier.duree)
    s_bouclier = Sort(p1,
                      conditions=[],
                      applications=[ajouter_etat(etat_bouclier)])
    assert len(p1.etats) == 0
    terrain.start()
    p1.lancer_sort(5, 5)
    assert p1.etats[0] == etat_bouclier
    assert p1.etats[0].duree == 3
    terrain.fin_de_tour()
    assert p1.etats[0] == etat_bouclier
    assert p1.etats[0].duree == 2
    terrain.fin_de_tour()
    assert p1.etats[0] == etat_bouclier
    assert p1.etats[0].duree == 1
    terrain.fin_de_tour()
    assert len(p1.etats) == 0


def test_fonctionnement_bouclier(terrain, p1, s_bouclier, p2, s2):
    terrain.start()
    assert p1.pv == 50
    terrain.fin_de_tour()
    p2.lancer_sort(5, 5)
    assert p1.pv == 47
    terrain.fin_de_tour()
    assert len(p1.etats) == 0
    p1.lancer_sort(5, 5)
    assert len(p1.etats) == 1
    assert p1.etats[0].duree == 3
    terrain.fin_de_tour()

    p2.lancer_sort(5, 5)
    assert p1.pv == 46
    terrain.fin_de_tour()
    assert p1.etats[0].duree == 2
    terrain.fin_de_tour()

    p2.lancer_sort(5, 5)
    assert p1.pv == 45
    terrain.fin_de_tour()
    assert p1.etats[0].duree == 1
    terrain.fin_de_tour()

    p2.lancer_sort(5, 5)
    assert p1.pv == 44
    terrain.fin_de_tour()
    assert len(p1.etats) == 0
    terrain.fin_de_tour()


    p2.lancer_sort(5, 5)
    assert p1.pv == 41


def test_precision(terrain, p1, s1, s_precision):
    assert s1.portee == 1
    assert p1.x, p1.y == (5, 5)
    terrain.start()
    
    p1.lancer_sort(6, 5) # 1 case.
    assert p1.pa == 5
    assert p1.pm == 2
    terrain.fin_de_tour()

    p1.lancer_sort(7, 5) # 2 case.
    assert p1.pa == 6
    assert p1.pm == 3
    terrain.fin_de_tour()

    p1.selectionner_sort(1)
    p1.lancer_sort(5, 5)
    p1.selectionner_sort(0)
    for _ in range(3):
        p1.lancer_sort(7, 4) # 3 cases.
        assert p1.pa == 5
        assert p1.pm == 2
        terrain.fin_de_tour()
    
    p1.lancer_sort(7, 5)
    assert p1.pa == 6
    assert p1.pm == 3





























if __name__ == "__main__":
    nom_script = sys.argv[0].split("/")[-1]
    msg = os.popen("pytest " + nom_script)# -vv")
    print(msg.read())
