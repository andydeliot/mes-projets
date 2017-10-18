# coding: utf-8

import os
from operateur import *
import pytest


# Setup.

@pytest.fixture()
def a():
    return Variable("a")

@pytest.fixture()
def b():
    return Variable("b")

@pytest.fixture()
def c():
    return Variable("c")

@pytest.fixture()
def d():
    return Variable("d")

@pytest.fixture()
def e():
    return Variable("e")

@pytest.fixture()
def taut():
    return Tautologie()

@pytest.fixture()
def cont():
    return Contradiction()


### formes.


# Teste variable.

def test_var(a):
    assert str(a) == "a"

def test_var_est(a, b):
    assert a.est(a)
    assert a.est(a + a)
    assert a.est(a * a)
    assert a.est(Variable("a"))

def test_var_est_autre(cont, a, b):
    assert not a.est(b)
    assert not a.est(taut)
    assert not a.est(cont)
    assert not a.est(-a)
    assert not a.est(a + b)
    assert not a.est(a * b)
    assert not a.est(a >> b)
    assert not a.est(a % b)
    assert not a.est(Variable("b"))


# Teste Tautologie.

def test_tautologie():
    assert str(Tautologie()) == "⏉"

def test_taut_est(taut):
    assert taut.est(Tautologie())

def test_est_autre(taut, cont, a, b):
    assert taut.est(cont) == False
    assert taut.est(a) == False
    assert taut.est(-a) == False
    assert taut.est(a + b) == False
    assert taut.est(a * b) == False
    assert taut.est(a >> b) == False
    assert taut.est(a % b) == False


# Teste Contraintes.

def test_contradiction():
    assert str(Contradiction()) == "⏊"

def test_cont_est(cont):
    assert cont.est(Contradiction())

def test_est_autre(taut, cont, a, b):
    assert cont.est(taut) == False
    assert cont.est(a) == False
    assert cont.est(-a) == False
    assert cont.est(a + b) == False
    assert cont.est(a * b) == False
    assert cont.est(a >> b) == False
    assert cont.est(a % b) == False


# Teste Négatif.

def test_negatif(a, b):
    assert str(-a) == "¬a"
    assert str(a + -b) == "a ˅ ¬b"
    assert str(a * -b) == "a ˄ ¬b"
    assert str(--a) == "a"

def test_involuer(a, b, c, d):
    assert str((--a).involuer()) == "a"
    assert str((---a).involuer()) == "¬a"
    assert str(((a * (b + ( c * ---d)))).involuer()) == "a ˄ (b ˅ (c ˄ ¬d))"

def test_neg_est(a, b):
    assert (-a).est(-a)
    assert (-a).est(Negatif(a))

def test_neg_est_autre(a, b):
    assert not (-a).est(-b)
    assert not (-a).est(a)
    assert not (-a).est(a + b)
    assert not (-a).est(a * b)
    assert not (-a).est(a >> b)
    assert not (-a).est(a % b)
    assert not (-a).est(Negatif(b))


# Teste Or.

def test_or(a, b):
    assert str(a + b) == "a ˅ b"

def test_or_association(a, b, c, d):
    assert str((a + b + c).associer()) == "a ˅ b ˅ c"
    assert str((a + (b + c)).associer()) == "a ˅ b ˅ c"
    assert str(((a + b) + (c + d)).associer()) == "a ˅ b ˅ c ˅ d"
    assert str((a + (b + (c + d))).associer()) == "a ˅ b ˅ c ˅ d"

def test_or_est(a, b, c, d, e):
    assert (a + b).est(a + b)
    assert (a + b + c + d).est(a + b + c + d)
    assert (a + b + c + d).est(b + d + a + c)
    assert (a + b + c + d).est(Or(*[a, b, c, d]))

def test_or_est_autre(taut, cont, a, b, c, d, e):
    assert not (a + b).est(taut)
    assert not (a + b).est(cont)
    assert not (a + b).est(a)
    assert not (a + b).est(-a)
    assert not (a + b).est(a * b)
    assert not (a + b).est(a >> b)
    assert not (a + b).est(a % b)
    assert not (a + b + c + d).est(a + b + c + d + e)
    assert not (a + b + c + d).est(a + b + c + e)
    assert not (a + b).est(Or(*[c, d]))


# Teste And.

def test_and(a, b):
    assert str(a * b) == "a ˄ b"

def test_and_association(a, b, c, d):
    assert str((a * b * c).associer()) == "a ˄ b ˄ c"
    assert str((a * (b * c)).associer()) == "a ˄ b ˄ c"
    assert str(((a * b) * (c * d)).associer()) == "a ˄ b ˄ c ˄ d"
    assert str((a * (b * (c * d))).associer()) == "a ˄ b ˄ c ˄ d"

def test_and_est(a, b, c, d, e):
    assert (a * b).est(a * b)
    assert (a * b * c * d).est(a * b * c * d)
    assert (a * b * c * d).est(b * d * a * c)
    assert (a * b).est(And(*[a, b]))

def test_and_est_autre(taut, cont, a, b, c, d, e):
    assert not (a * b).est(taut)
    assert not (a * b).est(cont)
    assert not (a * b).est(a)
    assert not (a * b).est(-a)
    assert not (a * b).est(a + b)
    assert not (a * b).est(a >> b)
    assert not (a * b).est(a % b)
    assert not (a * b * c * d).est(a * b * c * d * e)
    assert not (a * b * c * d).est(a * b * c * e)
    assert not (a * b).est(And(*[c, d]))


# Test Implication.

def test_implication(a, b, c):
    assert str((a >> b)) == "a ⇒ b"
    assert str((a >> b >> c)) == "(a ⇒ b) ⇒ c"

def test_implication_priorite_(a, b, c):
    assert str((a + b >> c)) == "(a ˅ b) ⇒ c"
    assert str((a >> b + c)) == "a ⇒ (b ˅ c)"
    assert str((a * b >> c)) == "(a ˄ b) ⇒ c"
    assert str((a >> b * c)) == "a ⇒ (b ˄ c)"
    assert str((a * (b >> c))) == "a ˄ (b ⇒ c)"

def test_implication_est_(a, b, c):
    assert (a >> b).est(a >> b)
    assert ((a * b) >> c).est((a * b) >> c)
    assert (a >> b).est(Implication(a, b))

def test_implication_est_autre(taut, cont, a, b, c, d):
    assert (a >> b).est(b >> a) == False
    assert (a >> b).est(a >> c) == False
    assert (a >> b).est(taut) == False
    assert (a >> b).est(cont) == False
    assert (a >> b).est(a) == False
    assert (a >> b).est(-a) == False
    assert (a >> b).est(a + b) == False
    assert (a >> b).est(a * b) == False
    assert (a >> b).est(a % b) == False
    assert not (a >> b).est(Implication(c, d))


# Teste double Implication.

def test_double_implication(a, b, c):
    assert str((a % b)) == "a ⇔ b"
    assert str((a % b % c)) == "(a ⇔ b) ⇔ c"

def test_double_implication_est(a, b, c):
    assert (a % b).est(a % b)
    assert (a % b).est(b % a)
    assert ((a % b) % (b % a)).est((a % b) % (b % a))
    assert (a % b).est(DoubleImplication(a, b))

def test_double_implication_est_autre(a, b, c, d):
    assert (a % b).est(a % c) == False
    assert (a % b).est(a) == False
    assert (a % b).est(-a) == False
    assert (a % b).est(a + b) == False
    assert (a % b).est(a * b) == False
    assert (a % b).est(a >> b) == False
    assert not (a % b).est(DoubleImplication(c, d))


# Teste création spéciales.

def test_priorite_and_or(a, b, c):
    assert str((a * b + c)) == "(a ˄ b) ˅ c"
    assert str((a + b * c)) == "a ˅ (b ˄ c)"

def test_creation(a, b, c, d, e):
    assert str((a + (b + (c * d)))) == "a ˅ b ˅ (c ˄ d)"
    assert str((a * (b * (c + d)))) == "a ˄ b ˄ (c ˅ d)"
    assert str((a + b + (c * (d * e) + (a * b)))) == "a ˅ (a ˄ b) ˅ b ˅ (c ˄ d ˄ e)"

def test_est_recursif(a, b, c, d):
    assert ((a + b) * (c >> d)).est((Variable("a") + Variable("b")) * (Variable("c") >> Variable("d")))


# Teste créations particulières.

def test_priorite_generale(a, b, c ,d ,e):
    assert str((a + b * c >> d % e)) == "(a ˅ (b ˄ c)) ⇒ (d ⇔ e)"
    assert str((a >> b * c % d + e)) == "a ⇒ (((b ˄ c) ⇔ d) ˅ e)"


# Les méthodes.

# Teste idempotance.

def test_idempotencer(cont, taut, a, b):
    assert str((cont * cont)) == "⏊"
    assert str((cont + cont)) == "⏊"
    assert str((taut * taut)) == "⏉"
    assert str((taut + taut)) == "⏉"
    assert str((a * a)) == "a"
    assert str((a + a)) == "a"
    assert str(a + a + a + (a * a * a)) == "a"
    assert str(b * (a + a)) == "a ˄ b"
    assert str(b + (a * a)) == "a ˅ b"
    assert str((a * b) + (a * b)) == "a ˄ b"
    assert str((a + b) * (a + b)) == "a ˅ b"
    assert str(a + b + b + a + b) == "a ˅ b"
    assert str(a * b * b * a * b) == "a ˄ b"
    assert str((a + a) >> (b * b)) == "a ⇒ b"


# Teste complémenter.

def test_complementer(a, b):
    assert str((a * -a).complementer()) == "⏊"
    assert str((a * -a * b).complementer()) == "b ˄ ⏊"
    assert str((a + -a).complementer()) == "⏉"
    assert str((a + -a + b).complementer()) == "b ˅ ⏉"
    assert str((a >> a).complementer()) == "⏉"
    assert str((a % a).complementer()) == "⏉"


# Teste neutraliser.

def test_neutraliser(cont, taut, a, b):
    assert str((a * taut).neutraliser()) == "a"
    assert str((a * b * taut).neutraliser()) == "a ˄ b"
    assert str((a + cont).neutraliser()) == "a"
    assert str((a + b + cont).neutraliser()) == "a ˅ b"
    assert str((taut >> a).neutraliser()) == "a"
    assert str((a >> cont).neutraliser()) == "¬a"
    assert str((a % taut).neutraliser()) == "a"
    assert str((taut % a).neutraliser()) == "a"
    assert str((a % cont).neutraliser()) == "¬a"
    assert str((cont % a).neutraliser()) == "¬a"


# Teste absorber.

def test_absorber(cont, taut, a, b):
    assert str((a + taut).absorber()) == "⏉"
    assert str((a + b + taut).absorber()) == "⏉"
    assert str((a * cont).absorber()) == "⏊"
    assert str((a * b * cont).absorber()) == "⏊"
    assert str((a >> taut).absorber()) == "⏉"
    assert str((cont >> a).absorber()) == "⏉"


# Teste distribuer.

def test_distribuer_or(a, b, c, d):
    assert str((a + (b * c)).distribuer_or()) == "(a ˅ b) ˄ (a ˅ c)"
    assert str((a + (b * c * d)).distribuer_or()) == "(a ˅ b) ˄ (a ˅ c) ˄ (a ˅ d)"
    assert str(((a + b) + (c * d)).distribuer_or()) == "(a ˅ b ˅ c) ˄ (a ˅ b ˅ d)"
    assert str((a + b + (c * d)).distribuer_or()) == "(a ˅ b ˅ c) ˄ (a ˅ b ˅ d)"
    assert str(((a * b) + c).distribuer_or()) == "(a ˅ c) ˄ (b ˅ c)"
    assert str((-a + (b * c)).distribuer_or()) == "(b ˅ ¬a) ˄ (c ˅ ¬a)"
    assert str((a + (b * c)).distribuer_and()) == "a ˅ (b ˄ c)"
    assert str((a + -(b * c)).distribuer_or()) == "a ˅ ¬(b ˄ c)"
    assert str((a * (b + (c * d))).distribuer_or()) == "a ˄ (b ˅ c) ˄ (b ˅ d)"
    assert str((a + (b * (c + d))).distribuer_or()) == "(a ˅ b) ˄ (a ˅ c ˅ d)"
    assert str(((a * b) + (c * d)).distribuer_or()) == "(a ˅ c) ˄ (a ˅ d) ˄ (b ˅ c) ˄ (b ˅ d)"

def test_distribuer_and(a, b, c, d):
    assert str((a * (b + c)).distribuer_and()) == "(a ˄ b) ˅ (a ˄ c)"
    assert str((a * (b + c + d)).distribuer_and()) == "(a ˄ b) ˅ (a ˄ c) ˅ (a ˄ d)"
    assert str(((a * b) * (c + d)).distribuer_and()) == "(a ˄ b ˄ c) ˅ (a ˄ b ˄ d)"
    assert str((a * b * (c + d)).distribuer_and()) == "(a ˄ b ˄ c) ˅ (a ˄ b ˄ d)"
    assert str(((a + b) * c).distribuer_and()) == "(a ˄ c) ˅ (b ˄ c)"
    assert str((-a * (b + c)).distribuer_and()) == "(b ˄ ¬a) ˅ (c ˄ ¬a)"
    assert str((a + (b * c)).distribuer_and()) == "a ˅ (b ˄ c)"
    assert str((a * -(b + c)).distribuer_and()) == "a ˄ ¬(b ˅ c)"
    assert str((a + (b * (c + d))).distribuer_and()) == "a ˅ (b ˄ c) ˅ (b ˄ d)"
    assert str((a * (b + (c * d))).distribuer_and()) == "(a ˄ b) ˅ (a ˄ c ˄ d)"
    assert str(((a + b) * (c + d)).distribuer_and()) == "(a ˄ c) ˅ (a ˄ d) ˅ (b ˄ c) ˅ (b ˄ d)"


# Teste Morgan.

def test_morgan(a, b, c):
    assert str((-(a + b)).morganiser()) == "¬a ˄ ¬b"
    assert str((-(a * b)).morganiser()) == "¬a ˅ ¬b"
    assert str((a * -(b + c)).morganiser()) == "a ˄ ¬b ˄ ¬c"
    assert str((-(a * (b + c))).morganiser()) == "¬a ˅ (¬b ˄ ¬c)"


# Teste Materialiser

def test_materialiser(a, b, c):
    assert str((a >> b).materialiser()) == "b ˅ ¬a"
    assert str(((a >> b) >> c).materialiser()) == "c ˅ ¬(b ˅ ¬a)"


# Teste Materialiser double.
def test_materialiser_double(a, b, c):
    assert str((a % b).materialiser_double()) == "(a ⇒ b) ˄ (b ⇒ a)"
    assert str(((a % b) % c).materialiser_double()) == "(((a ⇒ b) ˄ (b ⇒ a)) ⇒ c) ˄ (c ⇒ ((a ⇒ b) ˄ (b ⇒ a)))"
    

# Teste Normalisation.
def test_normaliser_exemple_implication(a, b, c, d):
    """ Exemple du cours de l'université Aix-Marseille, Licence 3 informatiques,
        logique propositionnelle, normalisation ˄ modélisation. """
    assert str(((-(a * (b >> (c + d)))) * (a + b)).normaliser()) == "(a ˅ b) ˄ (¬a ˅ ¬c) ˄ (¬a ˅ ¬d) ˄ (b ˅ ¬a)"
    assert str(((-(a * (-b + (c + d)))) * (a + b)).normaliser()) == "(a ˅ b) ˄ (¬a ˅ ¬c) ˄ (¬a ˅ ¬d) ˄ (b ˅ ¬a)"


# Teste pas de modification.
def test_pas_de_modification(a, b, c):
    f = a + b
    f + c
    assert str(f) == "a ˅ b"

def test_and_pas_de_modification(a, b, c):
    f = a * b
    f * c
    assert str(f) == "a ˄ b"

def test_involuer_pas_de_modification(a):
    f = a
    -f
    assert str(f) == "a"

def test_or_distribuer_pas_de_modification(a, b, c):
    f = a + (b * c)
    f.distribuer_or()
    assert str(f) == "a ˅ (b ˄ c)"

def test_or_distribuer_pas_de_modification2(a, b, c, d):
    f = (-(a * (b >> (c + d)))) * (a + b)
    f.distribuer_or()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇒ (c ˅ d)))"

def test_and_distribuer_pas_de_modification(a, b, c):
    f = a * (b + c)
    f.distribuer_and()
    assert str(f) == "a ˄ (b ˅ c)"

def test_and_distribuer_pas_de_modification2(a, b, c, d):
    f = (-(a * (b >> (c + d)))) * (a + b)
    f.distribuer_and()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇒ (c ˅ d)))"

def test_morgan_or_pas_de_modification(a, b):
    f = -(a + b)
    f.morganiser()
    assert str(f) == "¬(a ˅ b)"

def test_morgan_and_pas_de_modification(a, b):
    f = -(a * b)
    f.morganiser()
    assert str(f) == "¬(a ˄ b)"

def test_morgan_pas_de_modification2(a, b, c, d):
    f = (-(a * (b >> (c + d)))) * (a + b)
    f.morganiser()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇒ (c ˅ d)))"

def test_implication_pas_de_modification(a, b, c):
    f = a >> b
    f >> c
    assert str(f) == "a ⇒ b"

def test_double_implication_pas_de_modification(a, b, c):
    f = a % b
    f % c
    assert str(f) == "a ⇔ b"

def test_materialiser_pas_de_modification(a, b):
    f = a >> b
    f.materialiser()
    assert str(f) == "a ⇒ b"

def test_materialiser_pas_de_modification2(a, b, c, d):
    f = (-(a * (b >> (c + d)))) * (a + b)
    f.materialiser()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇒ (c ˅ d)))"

def test_materialiser_double_pas_de_modification(a, b):
    f = a % b
    f.materialiser_double()
    assert str(f) == "a ⇔ b"

def test_materialiser_double_pas_de_modification2(a, b, c, d):
    f = (-(a * (b % (c + d)))) * (a + b)
    f.materialiser_double()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇔ (c ˅ d)))"

def test_normaliser_pas_de_modification(a, b, c, d):
    f = (-(a * (b >> (c + d)))) * (a + b)
    f.normaliser()
    assert str(f) == "(a ˅ b) ˄ ¬(a ˄ (b ⇒ (c ˅ d)))"


# Teste recherche de variables.

def test_rechercher_variables(a, b, c, d, taut, cont):
    assert a.rechercher_variables() == [a]
    assert taut.rechercher_variables() == []
    assert cont.rechercher_variables() == []
    assert (-a).rechercher_variables() == [a]
    assert (-(a * b)).rechercher_variables() == [a, b]
    assert (a * b * c).rechercher_variables() == [a, b, c]
    assert (a + b + c).rechercher_variables() == [a, b, c]
    assert (a >> b).rechercher_variables() == [a, b]
    assert (a % b).rechercher_variables() == [a, b]
    assert ((a + b) * (c + d)).rechercher_variables() == [a, b, c, d]
    assert (a >> (a * b)).rechercher_variables() == [a, b]
    assert ((-(a * (b >> (c + d)))) * (a + b)).rechercher_variables() == [a, b, c, d]

def test_variables(a, b, c, d, taut, cont):
    assert a.variables == [a]
    assert taut.variables == []
    assert cont.variables == []
    assert (-a).variables == [a]
    assert (-(a * b)).variables == [a, b]
    assert (a * b * c).variables == [a, b, c]
    assert (a + b + c).variables == [a, b, c]
    assert (a >> b).variables == [a, b]
    assert (a % b).variables == [a, b]
    assert ((a + b) * (c + d)).variables == [a, b, c, d]
    assert (a >> (a * b)).variables == [a, b]
    assert ((-(a * (b >> (c + d)))) * (a + b)).variables == [a, b, c, d]


# Teste sur les calcules.

def teste_calcule_variable(a):
    assert a.calculer() == None
    a.valeur = False
    assert not a.calculer()
    a.valeur = True
    assert a.calculer()

def teste_calcule_negatif(a):
    assert (-a).calculer() == None
    a.valeur = False
    assert (-a).calculer()
    a.valeur = True
    assert not (-a).calculer()

def teste_calcule_or(a, b):
    f = a + b
    assert f.calculer() == None
    a.valeur = False
    assert f.calculer() == None
    a.valeur = True
    assert f.calculer()

    a.valeur, b.valeur = False, False
    assert f.calculer() == False
    b.valeur = True
    assert f.calculer()
    a.valeur = True
    b.valeur = False
    assert f.calculer()
    b.valeur = True
    assert f.calculer()

def teste_calcule_and(a, b):
    f = a * b
    assert f.calculer() == None
    a.valeur = True
    assert f.calculer() == None
    a.valeur = False
    assert not f.calculer()

    a.valeur, b.valeur = False, False
    assert f.calculer() == False
    b.valeur = True
    assert f.calculer() == False
    a.valeur = True
    b.valeur = False
    assert f.calculer() == False
    b.valeur = True
    assert f.calculer()

def teste_calcule_implication(a, b):
    f = a >> b
    assert f.calculer() == None
    a.valeur = True
    assert f.calculer() == None
    a.valeur = False
    assert f.calculer()

    a.valeur, b.valeur = False, False
    assert f.calculer()
    b.valeur = True
    assert f.calculer()
    a.valeur = True
    b.valeur = False
    assert f.calculer() == False
    b.valeur = True
    assert f.calculer()

def teste_calcule_double_implication(a, b):
    f = a % b
    assert f.calculer() == None
    a.valeur = False
    assert f.calculer() == None
    a.valeur = True
    assert f.calculer() == None

    a.valeur, b.valeur = False, False
    assert f.calculer()
    b.valeur = True
    assert f.calculer() == False
    a.valeur = True
    b.valeur = False
    assert f.calculer() == False
    b.valeur = True
    assert f.calculer()


# Afficher valeur.

def test_afficher_valeur(a, b, cont, taut):
    assert a.afficher_valeur() == "x"
    a.valeur = False
    assert a.afficher_valeur() == "0"
    b.valeur = True
    assert b.afficher_valeur() == "1"
    assert cont.afficher_valeur() == "0"
    assert taut.afficher_valeur() == "1"
    assert (-a).afficher_valeur() == "1"
    assert (a + b).afficher_valeur() == "1"
    assert (a * b).afficher_valeur() == "0"
    assert (a >> b).afficher_valeur() == "1"
    assert (a % b).afficher_valeur() == "0"


# Afficher valence.

def test_afficher_valence(a, b, cont, taut):
    assert a.afficher_valence() == "x | x"
    a.valeur = False
    assert a.afficher_valence() == "0 | 0"
    b.valeur = True
    assert b.afficher_valence() == "1 | 1"
    assert taut.afficher_valence() == "1"
    assert cont.afficher_valence() == "0"
    assert (-a).afficher_valence() == "0 | 1"
    assert (a + b).afficher_valence() == "0 1 | 1"
    assert (a * b).afficher_valence() == "0 1 | 0"
    assert (a >> b).afficher_valence() == "0 1 | 1"
    assert (a % b).afficher_valence() == "0 1 | 0"


# Valeur suivante.

def test_valeur_suivante(a, b, c, d, cont, taut):
    for var in [a, b, c, d]:
        var.valeur = False
    a.valeur_suivante()
    assert a.valeur == True
    b.valeur = True
    b.valeur_suivante()
    assert b.valeur == False
    f1 = c + d
    assert c.valeur == False
    assert d.valeur == False
    f1.valeur_suivante()
    assert c.valeur == False
    assert d.valeur
    cont.valeur_suivante()
    taut.valeur_suivante()
    assert c.valeur == False
    assert d.valeur

def test_valeur_suivante_generateur(a, b, c, d, cont, taut):
    assert a.valeur_suivante()
    assert a.valeur_suivante() == False
    assert (-b).valeur_suivante()
    assert (-b).valeur_suivante() == False
    f1 = c + d
    assert f1.valeur_suivante()
    assert f1.valeur_suivante()
    assert f1.valeur_suivante()
    assert f1.valeur_suivante() == False

# Afficher variables.

def test_afficher_variables(a, b, c, d, cont, taut):
    assert a.afficher_variables() == "a | a"
    b.valeur = False
    assert b.afficher_variables() == "b | b"
    assert taut.afficher_variables() == "⏉"
    assert cont.afficher_variables() == "⏊"
    assert (-a).afficher_variables() == "a | ¬a"
    assert (a + b).afficher_variables() == "a b | a ˅ b"
    assert (a * b).afficher_variables() == "a b | a ˄ b"
    assert (a >> b).afficher_variables() == "a b | a ⇒ b"
    assert (a % b).afficher_variables() == "a b | a ⇔ b"
    assert ((a * c) + (b * d)).afficher_variables() == "a b c d | (a ˄ c) ˅ (b ˄ d)"


# Afficher table.

def test_afficher_table(a, b, c, d, cont, taut):
    assert a.afficher_table() == "a | a\n-----\n0 | 0\n1 | 1"
    b.valeur = False
    assert b.afficher_table() == "b | b\n-----\n0 | 0\n1 | 1"
    assert taut.afficher_table() == "⏉\n-\n1"
    assert cont.afficher_table() == "⏊\n-\n0"
    assert (-a).afficher_table() == "a | ¬a\n------\n0 | 1\n1 | 0"
    assert (a + b).afficher_table() == "a b | a ˅ b\n-----------\n0 0 | 0\n0 1 | 1\n1 0 | 1\n1 1 | 1"
    assert (a * b).afficher_table() == "a b | a ˄ b\n-----------\n0 0 | 0\n0 1 | 0\n1 0 | 0\n1 1 | 1"
    assert (a >> b).afficher_table() == "a b | a ⇒ b\n-----------\n0 0 | 1\n0 1 | 1\n1 0 | 0\n1 1 | 1"
    assert (a % b).afficher_table() == "a b | a ⇔ b\n-----------\n0 0 | 1\n0 1 | 0\n1 0 | 0\n1 1 | 1"
    assert ((a * c) + (b * d)).afficher_table() == "a b c d | (a ˄ c) ˅ (b ˄ d)\n---------------------------\n0 0 0 0 | 0\n0 0 0 1 | 0\n0 0 1 0 | 0\n0 0 1 1 | 0\n0 1 0 0 | 0\n0 1 0 1 | 1\n0 1 1 0 | 0\n0 1 1 1 | 1\n1 0 0 0 | 0\n1 0 0 1 | 0\n1 0 1 0 | 1\n1 0 1 1 | 1\n1 1 0 0 | 0\n1 1 0 1 | 1\n1 1 1 0 | 1\n1 1 1 1 | 1"

# Afficher modèle.

def test_afficher_modele(a, b, c, d, cont, taut):
    assert a.afficher_modele() == "a | a\n-----\n1 | 1"
    b.valeur = False
    assert b.afficher_modele() == "b | b\n-----\n1 | 1"
    assert taut.afficher_modele() == "⏉\n-\n1"
    assert (-a).afficher_modele() == "a | ¬a\n------\n0 | 1"
    assert (a + b).afficher_modele() == "a b | a ˅ b\n-----------\n0 1 | 1\n1 0 | 1\n1 1 | 1"
    assert (a * b).afficher_modele() == "a b | a ˄ b\n-----------\n1 1 | 1"
    assert (a >> b).afficher_modele() == "a b | a ⇒ b\n-----------\n0 0 | 1\n0 1 | 1\n1 1 | 1"
    assert (a % b).afficher_modele() == "a b | a ⇔ b\n-----------\n0 0 | 1\n1 1 | 1"
    assert ((a * c) + (b * d)).afficher_modele() == "a b c d | (a ˄ c) ˅ (b ˄ d)\n---------------------------\n0 1 0 1 | 1\n0 1 1 1 | 1\n1 0 1 0 | 1\n1 0 1 1 | 1\n1 1 0 1 | 1\n1 1 1 0 | 1\n1 1 1 1 | 1"






















if __name__ == "__main__":
    msg = os.popen("py.test")# -vv")
    print(msg.read())
