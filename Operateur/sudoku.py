from operateur import *
from random import choice
import cProfile


def element_fonctionne(formule, var):
    """ Retourne vrai si tout les éléments contenant var renvoie vrai lors du calcule. Faux sinon. """
    resultat = True
    for element in formule.elements:
        if var in element.variables:
            if element.calculer() == False:
                return False
    return resultat


def quine(formule, num_var=0):
    if num_var >= len(formule.variables):
        print(formule.afficher_valence())
        return True
    else:
        var = formule.variables[num_var]

        var.valeur = False
        if element_fonctionne(formule, var):
            if quine(formule, num_var+1):
                return True
            else:
                pass

        var.valeur = True
        if element_fonctionne(formule, var):
            if quine(formule, num_var+1):
                return True
            else:
                pass

        var.valeur = None

def quine2(formule, num_var=0):
    if num_var >= len(formule.variables):
        print(formule.afficher_valence())
    else:
        var = formule.variables[num_var]

        var.valeur = False
        if element_fonctionne(formule, var):
            quine(formule, num_var+1)

        var.valeur = True
        if element_fonctionne(formule, var):
            quine(formule, num_var+1)

        var.valeur = None

def retrouver_variable(variables, nom):
    """ Retrouve une variable par son nom. """
    for var in variables:
        if var.nom == nom:
            return var
    return None

if __name__ == "__main__":
##    profileur = cProfile.Profile()
##    profileur.enable()

    # Méta-data.
    long = range(1, 5)
    
    # Génération des variables.
    variables = []
    for i in long:
        for j in long:
            for k in long:
                variables.append(Variable("{0}{1}{2}".format(i, j, k)))
    print(variables)
    print(len(variables))

    # Génération des formules.
    # Chaque case ne contient qu'une valeur.
    valeur_unique = []
    for i in long:
        for j in long:
            sous_valeur_unique = []
            for k1 in long:
                v1 = retrouver_variable(variables, "{0}{1}{2}".format(i, j, k1))
                k2s = []
                for k2 in long:
                    if k1 != k2:
                        v2 = retrouver_variable(variables, "{0}{1}{2}".format(i, j, k2))
                        k2s.append(-v2)
                sous_valeur_unique.append(And(v1, *[k2 for k2 in k2s]))
            valeur_unique.append(Or(*[formule for formule in sous_valeur_unique]))

    f1 = And(*[formule for formule in valeur_unique])

    f1 = f1.distribuer_or()
    print("Distribution ok")
    # Chaque colone ne contient qu'une valeur.
    colone_valeur_unique = []
    for k in long:
        for i in long:
            for j1 in long:
                v1 = retrouver_variable(variables, "{0}{1}{2}".format(i, j1, k))
                for j2 in long:
                    if j1 != j2:
                        v2 = retrouver_variable(variables, "{0}{1}{2}".format(i, j2, k))
                        colone_valeur_unique.append(v1 >> -v2)

    f2 = And(*[formule for formule in colone_valeur_unique])

    # Chaque ligne ne contient qu'une valeur.
    ligne_valeur_unique = []
    for k in long:
        for j in long:
            for i1 in long:
                v1 = retrouver_variable(variables, "{0}{1}{2}".format(i1, j, k))
                for i2 in long:
                    if i1 != i2:
                        v2 = retrouver_variable(variables, "{0}{1}{2}".format(i2, j, k))
                        ligne_valeur_unique.append(v1 >> -v2)

    f3 = And(*[formule for formule in ligne_valeur_unique])

    # Grille donnée.
    v1 = retrouver_variable(variables, "{0}{1}{2}".format(1, 1, 3))
    v2 = retrouver_variable(variables, "{0}{1}{2}".format(1, 2, 2))
    v3 = retrouver_variable(variables, "{0}{1}{2}".format(2, 3, 1))
    f4 = v1 * v2 * v3

    f_final = f1 * f2 * f3 * f4
    f_final = f_final.normaliser()
    print("Normaliser ok")
    f_final = f_final.complementer()
    f_final = f_final.absorber()
    f_final = f_final.absorber()
    f_final = f_final.neutraliser()

    print("Début algorithme")

    # Résolution aléatoire.
    if False:
        contraintes = len(f_final.elements)
        essai = 0
        while not f_final.calculer():
            if essai > 800:
                for var in f_final.variables:
                    var.valeur = False
                    print(var)
                print(f_final.afficher_valence())
                essai = 0
                contraintes = len(f_final.elements)

            variables = [choice(f_final.variables) for _ in range(1)]
            for var in variables:
                var.valeur = not var.valeur

            contrainte_non_respecte = 0
            for formule in f_final.elements:
                if not formule.calculer():
                    contrainte_non_respecte += 1

            if contrainte_non_respecte <= contraintes:
                contraintes = contrainte_non_respecte
            else:
                for var in variables:
                    var.valeur = not var.valeur
            essai += 1

            print("Contraintes : ", contraintes, essai)
    # Algorithme de Quine
    else:
        quine2(f_final)
    
##    profileur.disable()
##    profileur.create_stats()
##    profileur.print_stats()
##


















