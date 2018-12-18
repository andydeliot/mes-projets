# coding: utf-8

import os
import pytest
import sys


from Graphes import Tache, Graphe, taches

# Fixtures

@pytest.fixture()
def A():
    return Tache("Une nouvelle tâche", 1)

@pytest.fixture()
def B(A):
    return Tache("Une deuxième tâche", 2, A)

@pytest.fixture()
def C(A):
    return Tache("Une troisième tâche", 3, A)

@pytest.fixture()
def D( B, C):
    return Tache("Une quatrième tâche", 4, B, C)

@pytest.fixture()
def E(A, B):
    return Tache("Une cinquième tâche", 5, A, B)

@pytest.fixture()
def F(A, C, D):
    return Tache("Une sixième tâche", 6, A, C, D)

@pytest.fixture()
def Gphe(A, B, C, D, E, F):
    return Graphe(A, B, C, D, E, F)



# Tests

def test_nouvelle_tache(A):
    assert A.nom == "Une nouvelle tâche"
    assert A.duree == 1
    assert A.predecesseurs == []
    assert str(A) == "Une nouvelle tâche (1) []"

def test_tache_avec_predecesseurs(A, B, C):
    assert B.nom == "Une deuxième tâche"
    assert B.duree == 2
    assert B.predecesseurs == [A]
    assert str(B) == "Une deuxième tâche (2) [Une nouvelle tâche]"
    assert C.nom == "Une troisième tâche"
    assert C.duree == 3
    assert C.predecesseurs == [A]
    assert str(C) == "Une troisième tâche (3) [Une nouvelle tâche]"

def test_tache_deux_predecesseurs(B, C, D):
    assert D.nom == "Une quatrième tâche"
    assert D.duree == 4
    assert D.predecesseurs == [B, C]
    assert str(D) == "Une quatrième tâche (4) [Une deuxième tâche, Une troisième tâche]"

def test_successeurs(A, B, C, D):
    assert A.successeurs == [B, C]
    assert B.successeurs == [D]
    assert C.successeurs == [D]
    assert D.successeurs == []



def test_recherche_predecesseur(A, B, C, D):
    assert D.recherche_predecesseur(A) == True
    assert D.recherche_predecesseur(B) == True
    assert D.recherche_predecesseur(C) == True
    assert D.recherche_predecesseur(D) == True
    assert C.recherche_predecesseur(A) == True
    assert C.recherche_predecesseur(B) == False
    assert C.recherche_predecesseur(C) == True
    assert C.recherche_predecesseur(D) == False
    assert B.recherche_predecesseur(A) == True
    assert B.recherche_predecesseur(B) == True
    assert B.recherche_predecesseur(C) == False
    assert B.recherche_predecesseur(D) == False
    assert A.recherche_predecesseur(A) == True
    assert A.recherche_predecesseur(B) == False
    assert A.recherche_predecesseur(C) == False
    assert A.recherche_predecesseur(D) == False
def test_recherche_successeur(A, B, C, D):
    assert D.recherche_successeur(A) == False
    assert D.recherche_successeur(B) == False
    assert D.recherche_successeur(C) == False
    assert D.recherche_successeur(D) == True
    assert C.recherche_successeur(A) == False
    assert C.recherche_successeur(B) == False
    assert C.recherche_successeur(C) == True
    assert C.recherche_successeur(D) == True
    assert B.recherche_successeur(A) == False
    assert B.recherche_successeur(B) == True
    assert B.recherche_successeur(C) == False
    assert B.recherche_successeur(D) == True
    assert A.recherche_successeur(A) == True
    assert A.recherche_successeur(B) == True
    assert A.recherche_successeur(C) == True
    assert A.recherche_successeur(D) == True

def test_anti_transitivite_simple(A, B, C, D, E, F):
    assert E.predecesseurs == [B]
    assert F.predecesseurs == [D]

def test_date_au_plus_tot(A, B, C, D, E, F):
    Gphe = Graphe(A, B, C, D, E, F)
    assert Gphe.debut.date_plus_tot == 0
    assert A.date_plus_tot == 0
    assert B.date_plus_tot == 1
    assert C.date_plus_tot == 1
    assert D.date_plus_tot == 4
    assert E.date_plus_tot == 3
    assert F.date_plus_tot == 8
    assert Gphe.fin.date_plus_tot == 14

def test_date_au_plus_tard(A, B, C, D, E, F, Gphe):
    assert Gphe.debut.date_plus_tard == 0
    assert A.date_plus_tard == 0
    assert B.date_plus_tard == 2
    assert C.date_plus_tard == 1
    assert D.date_plus_tard == 4
    assert E.date_plus_tard == 9
    assert F.date_plus_tard == 8
    assert Gphe.fin.date_plus_tot == 14

def test_affichage_tableau(A, B, C, D, E, F, Gphe):
    assert A.affichage_tableau() == "Une nouvelle tâche (1) 0/0"
    assert B.affichage_tableau() == "Une deuxième tâche (2) 1/2"
    assert C.affichage_tableau() == "Une troisième tâche (3) 1/1"
    assert D.affichage_tableau() == "Une quatrième tâche (4) 4/4"
    assert E.affichage_tableau() == "Une cinquième tâche (5) 3/9"
    assert F.affichage_tableau() == "Une sixième tâche (6) 8/8"

def test_graphe(A, B, C, D, E, F, Gphe):

    assert Gphe.debut.predecesseurs == []
    assert A.predecesseurs == [Gphe.debut]
    assert B.predecesseurs == [A]
    assert C.predecesseurs == [A]
    assert D.predecesseurs == [B, C]
    assert E.predecesseurs == [B]
    assert F.predecesseurs == [D]
    assert Gphe.fin.predecesseurs == [E, F]

    assert Gphe.debut.successeurs == [A]
    assert A.successeurs == [B, C]
    assert B.successeurs == [D, E]
    assert C.successeurs == [D]
    assert D.successeurs == [F]
    assert E.successeurs == [Gphe.fin]
    assert F.successeurs == [Gphe.fin]
    assert Gphe.fin.successeurs == []

def test_affichage_tableau_graphe(A, B, C, D, E, F, Gphe):
    assert Gphe.affichage_tableau() == """Nom | Durée | Date au plus tôt/Date au plus tard
Une nouvelle tâche (1) 0/0
Une deuxième tâche (2) 1/2
Une troisième tâche (3) 1/1
Une quatrième tâche (4) 4/4
Une cinquième tâche (5) 3/9
Une sixième tâche (6) 8/8
Fin (0) 14/14"""

def test_chemin_critique(A, B, C, D, E, F, Gphe):
    assert Gphe.chemin_critique == [Gphe.fin, F, D, C, A, Gphe.debut]

def test_listage_predecesseur(A, B, C, D, E, F, Gphe):
    assert Gphe.debut.listage_predecesseurs() == [Gphe.debut]
    assert A.listage_predecesseurs() == [Gphe.debut, A]
    assert B.listage_predecesseurs() == [Gphe.debut, A, B]
    assert C.listage_predecesseurs() == [Gphe.debut, A, C]
    assert D.listage_predecesseurs() == [Gphe.debut, A, B, C, D]
    assert E.listage_predecesseurs() == [Gphe.debut, A, B, E]
    assert F.listage_predecesseurs() == [Gphe.debut, A, B, C, D, F]
    assert Gphe.fin.listage_predecesseurs() == [Gphe.debut, A, B, E, C, D, F, Gphe.fin]


def test_volume_tache(A, B, C, D, E, F):
    assert A.volume() == 1
    assert B.volume() == 3
    assert C.volume() == 4
    assert D.volume() == 10
    assert E.volume() == 8
    assert F.volume() == 16


def test_volume_graphe(A, B, C, D, E, F, Gphe):
    assert Gphe.volume() == Gphe.fin.volume()
    assert Gphe.volume() == 21

##def test_calcul_marge():
##    A = Tache("", 5)
##    A.date_plus_tot = 0
##    A.date_plus_tard = 5
##    assert A.calcul_marge() == 0
##    A.date_plus_tard = 10
##    assert A.calcul_marge() == 5
##    A.date_plus_tard = 3
##    assert A.calcul_marge() == 2

def test_dot_tache(A):
    assert A.dot() == """\t"Une nouvelle tâche" [color=red, style=filled];
\t"Une nouvelle tâche";
"""


def test_dot_tache_avec_successeur(A, B, C):
    assert A.dot() == """\t"Une nouvelle tâche" [color=red, style=filled];
\t"Une nouvelle tâche" -> "Une deuxième tâche", "Une troisième tâche";
"""
    B.date_plus_tot = 1
    B.date_plus_tard = 2
    assert B.dot() == """\t"Une deuxième tâche";
\t"Une deuxième tâche";
"""
    C.date_plus_tot = 1
    C.date_plus_tard = 1
    assert C.dot() == """\t"Une troisième tâche" [color=red, style=filled];
\t"Une troisième tâche";
"""


def test_dot_graphe(A):
    Gphe = Graphe(A)
    assert Gphe.dot() == """digraph Gphe {
\t"Début" [color=red, style=filled];
\t"Début" -> "Une nouvelle tâche";
\t"Une nouvelle tâche" [color=red, style=filled];
\t"Une nouvelle tâche" -> "Fin";
\t"Fin" [color=red, style=filled];
}"""


def test_generation_html_tache(A, B, C):
    assert A.generation_html() == """<tr><td>Une nouvelle tâche</td><td bgcolor="#FF5733"></tr>\n"""
    assert B.generation_html() == """<tr><td>Une deuxième tâche</td><td bgcolor="#FF5733"><td bgcolor="#FF5733"></tr>\n"""
    assert C.generation_html() == """<tr><td>Une troisième tâche</td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#FF5733"></tr>\n"""



def test_generation_html_graphe(A, B, C):
    Gphe = Graphe(A, B, C)
    print(Gphe.generation_html())
    assert Gphe.generation_html() == """<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<table border=5>
<tr><th>Nom de l'étape</th><th>0</th><th>1</th><th>2</th><th>3</th></tr>
<tr><td>Une nouvelle tâche</td><td bgcolor="#FF5733"><td><td><td></tr>
<tr><td>Une deuxième tâche</td><td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#3375FF"></tr>
<tr><td>Une troisième tâche</td><td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#FF5733"></tr>
</table>
"""

def test_generation_html_graphe2(A, B, C, D):
    Gphe = Graphe(A, B, C, D)
    print(Gphe.generation_html())
    assert Gphe.generation_html() == """<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<table border=5>
<tr><th>Nom de l'étape</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr>
<tr><td>Une nouvelle tâche</td><td bgcolor="#FF5733"><td><td><td><td><td><td><td></tr>
<tr><td>Une deuxième tâche</td><td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#3375FF"><td><td><td><td></tr>
<tr><td>Une troisième tâche</td><td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td><td><td><td></tr>
<tr><td>Une quatrième tâche</td><td><td><td><td><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#FF5733"><td bgcolor="#FF5733"></tr>
</table>
"""




















if __name__ == "__main__":
    nom_script = sys.argv[0].split("/")[-1]
    msg = os.popen("pytest-3 " + nom_script + " -vv")
    print(msg.read())
