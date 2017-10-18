
from itertools import product, combinations, combinations_with_replacement


# Objet.

class Element:
    def __init__(self):
        self.variables = []

    def est(self, other):
        """ Observe si deux éléments sont identiques. (a + b) = (Variable("a") + Variable("b")) """
        return self.__class__ is other.__class__

    def idempotencer(self):
        """ Réduit les éléments en récurrant. (a * a).idempotencer() = a """
        return self

    def complementer(self):
        """ Transforme en tautologie ou en contradiction des éléments opposés. (a * -a).complementer() = cont """
        return self

    def neutraliser(self):
        """ Supprime les tautologies ou les contradictions inutiles. (a * taut).neutraliser() = a """
        return self

    def absorber(self):
        """ Supprime les variables lorsque une contradiction ou une tautologie les absorbes. (a + taut).absorber() = taut """
        return self

    def associer(self):
        """ Associe les sous éléments de And ou de Or. (a * (b * c)).associer()) = a * b * c """
        return self

    def involuer(self):
        """ Supprime les négations récurrentes. (--a).involuer() = a """
        return self

    def distribuer_or(self):
        """ Renvoie la formule distribué par le Or. (a + (b * c)).distribuer_or() = (a + b) * (a + c) """
        return self

    def distribuer_and(self):
        """ Renvoie la formule distribué par le And. (a * (b + c)).distribuer_or() = (a * b) + (a * c) """
        return self

    def morganiser(self):
        """ Applique la négation aux sous-éléments. (-(a + b)).morganiser() = -a * -b """
        return self

    def materialiser(self):
        """ Materialise les implications. (a >> b).materialiser()) = -a + b """
        return self

    def materialiser_double(self):
        """ Materialise les doubles implications. (a % b).materialiser_double() = (a >> b) * (b >> a) """
        return self

    def normaliser(self):
        """ Fonction peu testé. Normalise une formule sous la forme And(*Or()) """
        #print("Formule initiale :                         " + str(self))
        self = self.materialiser_double()
        #print("Formule double implication materialisée :  " + str(self))
        self = self.materialiser()
        #print("Formule implication materialisée :         " + str(self))
        self = self.involuer()
        #print("Formule involuée :                         " + str(self))
        self = self.morganiser()
        #print("Formule morganisée :                       " + str(self))
        self = self.distribuer_or()
        #print("Formule distribuée :                       " + str(self))
        self = self.neutraliser()
        #print("Formule neutralisée :                      " + str(self))
        return self

    def resoudre(self):
        """ Fonction non testé. Simplifie la formule au maximum. """
        print("Formule initiale :                         " + str(self))
        self = self.materialiser_double()
        print("Formule double implication materialisée :  " + str(self))
        self = self.materialiser()
        print("Formule implication materialisée :         " + str(self))
        self = self.morganiser()
        print("Formule morganisée :                       " + str(self))
        self = self.distribuer_or()
        print("Formule distribuée :                       " + str(self))
        self = self.complementer().absorber().neutraliser()
        print("Formule simplifiée :                      " + str(self))
        return self

    def resoudre_libreoffice(self):
        """ Résoud et transforme le texte en texte libreoffice. """
        texte = "%rhô = " + self.formule_libreoffice() + " newline \n"
        self = self.materialiser_double()
        texte += "%rhô equiv " +self.formule_libreoffice() + " newline \n"
        self = self.materialiser()
        texte += "%rhô equiv " +self.formule_libreoffice() + " newline \n"
        self = self.morganiser()
        texte += "%rhô equiv " +self.formule_libreoffice() + " newline \n"
        self = self.distribuer_or()
        texte += "%rhô equiv " +self.formule_libreoffice() + " newline \n"
        self = self.complementer().absorber()
        texte += "%rhô equiv " +self.formule_libreoffice() + " \n"
        print(texte)
        return self

    def formule_libreoffice(self):
        """ Transforme le texte de la formule en texte libreoffice formule. """
        texte = str(self)
        texte2 = ""
        for lettre in texte:
            if lettre == "⏉":
                lettre = "T"
            elif lettre == "⏊":
                lettre = "Contradiction"
            elif lettre == "⇒":
                lettre = "drarrow"
            elif lettre == "⇔":
                lettre = "dlrarrow"
            texte2 += lettre
        return texte2

    def __add__(self, other):
        """ a + b = a ˅ b """
        return Or(self, other).associer().idempotencer().neutraliser()

    def __mul__(self, other):
        """ a * b = a ˄ b """
        return And(self, other).associer().idempotencer().neutraliser()

    def __neg__(self):
        """ -a = ¬a """
        return Negatif(self).involuer()

    def __rshift__(self, other):
        """ a >> b = a ⇒ b """
        return Implication(self, other)

    def __mod__(self, other):
        """ a % b = a ⇔ b """
        return DoubleImplication(self, other)

    def rechercher_variables(self):
        """ Retourne les variables contenue dans l'élément. """
        return []

    def calculer(self):
        """ Retourne une valeur booléenne, ou None s'il n'est pas possible de connaitre la valeur finale. """
        return None

    def afficher_formule(self):
        """ Affiche la formule complète. """
        return str(self)

    def afficher_valeur(self):
        """ Affiche la valeur de la formule avec "0" pour False et "1" pour True. a.valeur = False; a.afficher_valeur() = "0" """
        return "x" if self.calculer() is None else "1" if self.calculer() else "0"

    def afficher_valence(self):
        """ Affiche la valeur de chaque variable et la valeur de la formule. (a + b).afficher_valence() = "0 1 | 1" """
        affichage = ""
        for variable in self.variables:
            affichage += variable.afficher_valeur() + " "
        if len(self.variables):
            affichage += "| "
        affichage += self.afficher_valeur()
        return affichage

    def valeur_suivante(self):
        """ Change la valeur d'une variable pour générer une possibilité de plus. Retourne False si valeur_suivante à fait un tour. True sinon. """
        a = -1
        while a >= -len(self.variables):
            variable = self.variables[a]
            if variable.valeur:
                variable.valeur = False
                a -= 1
            else:
                variable.valeur = True
                return True
        return False

    def generer_table(self):
        """ Génère la table de vérité. Non testé."""
        while True :
            yield self.afficher_valence()
            if not self.valeur_suivante():
                break

    def generer_modele(self):
        """ Génère les modèles de la formule. Non testé."""
        while True :
            if self.calculer():
                yield self.afficher_valence()
            if not self.valeur_suivante():
                break

    def afficher_variables(self):
        """ Affiche les variables de la fonction ainsi que la fonction. (a + b).afficher_variables() = "a b | a ˅ b" """
        affichage = ""
        for variable in self.variables:
            affichage += variable.afficher_formule() + " "
        if len(self.variables):
            affichage += "| "
        affichage += self.afficher_formule()
        return affichage

    def afficher_table(self):
        """ Affiche la table de vérité de la formule. """
        for var in self.variables:
            var.valeur = False
        affichage = ""
        affichage += self.afficher_variables() + "\n"
        affichage += "-" * len(self.afficher_variables())
        for valence in self.generer_table():
            affichage += "\n" + valence
        return affichage

    def afficher_modele(self):
        """ Affiche les modèles de la formule. """
        affichage = ""
        affichage += self.afficher_variables() + "\n"
        affichage += "-" * len(self.afficher_variables())
        for valence in self.generer_table():
            if self.calculer():
                affichage += "\n" + valence
        return affichage

    def __str__(self):
        return self.afficher_formule()

    def __repr__(self):
        return str(self)

class Variable(Element):
    def __init__(self, nom, valeur=None):
        assert isinstance(nom, str), "L'élément donné est mauvais : " + element
        assert valeur in [True, False, None], "La valeur donné est mauvaise :" + valeur
        Element.__init__(self)
        self.variables = [self] #self.rechercher_variables()
        self.nom = nom
        self.valeur = valeur

    def est(self, other):
        if self.__class__ is not other.__class__:
            return False
        return self.nom == other.nom

    def calculer(self):
        return self.valeur

    def rechercher_variables(self):
        return [self]

    def afficher_formule(self):
        return self.nom

    def __lt__(self, other):
        if type(other) is Variable:
            return True if self.nom < other.nom else False
        else:
            return super.__lt__(self, other)

    def __gt__(self, other):
        if type(other) is Variable:
            return True if self.nom > other.nom else False
        else:
            return super.__gt__(self, other)

    def __eq__(self, other):
        if type(other) is Variable:
            return self.nom == other.nom
        else:
            return super.__eq__(self, other)


class Tautologie(Element):
    def __init__(self):
        Element.__init__(self)

    def calculer(self):
        return True

    def afficher_formule(self):
        return "⏉"


class Contradiction(Element):
    def __init__(self):
        Element.__init__(self)

    def calculer(self):
        return False

    def afficher_formule(self):
        return "⏊"


class Negatif(Element):
    def __init__(self, element):
        assert isinstance(element, Element), "L'élément donné est mauvais : " + element
        Element.__init__(self)
        self.element = element
        self.variables = self.rechercher_variables()

    def idempotencer(self):
        return -self.element.idempotencer()

    def complementer(self):
        return -self.element.complementer()

    def neutraliser(self):
        return -self.element.neutraliser()

    def absorber(self):
        return -self.element.absorber()

    def associer(self):
        return -self.element.associer()

    def involuer(self):
        if type(self.element) is Negatif:
            return self.element.element
        else:
            return Negatif(self.element.involuer())

    def distribuer_and(self):
        return -self.element.distribuer_and()

    def distribuer_or(self):
        return -self.element.distribuer_or()

    def morganiser(self):
        element_morganise = self.element.morganiser()
        if type(self.element) is Or:
            return And(*[-x for x in element_morganise.elements]).morganiser()
        if type(self.element) is And:
            return Or(*[-x for x in element_morganise.elements]).morganiser()
        return -element_morganise.associer()

    def materialiser(self):
        return -self.element.materialiser()

    def materialiser_double(self):
        return -self.element.materialiser_double()

    def est(self, other):
        if other.__class__ is Negatif:
            return True if self.element.est(other.element) else False
        else:
            return False

    def rechercher_variables(self):
        return self.element.rechercher_variables()

    def calculer(self):
        valeur = self.element.calculer()
        return valeur if valeur is None else not -valeur

    def afficher_formule(self):
        if isinstance(self.element, FormuleDeuxElement) or \
           isinstance(self.element, FormuleMultiElement):
            return "¬" + "(" + str(self.element) + ")"
        else:
            return "¬" + str(self.element)


class FormuleMultiElement(Element):
    def __init__(self, symbole, elements):
        assert len(elements) >= 2, "Il y a moins de 2 variables dans la formule."
        for element in elements:
            assert isinstance(element, Element), "Un élément donné est mauvais : " + str(args)
        Element.__init__(self)
        self.symbole = symbole
        self.elements = elements
        self.variables = self.rechercher_variables()

    def idempotencer(self):
        elmts = [element.idempotencer() for element in self.elements]
        nouveau_elmts = {}
        for elmt in elmts:
            nouveau_elmts[elmt.afficher_formule()] = elmt
        
        nouveau_elmts = list(nouveau_elmts.items())
        nouveau_elmts.sort()
        nouveau_elmts = [elmt[-1] for elmt in nouveau_elmts]

        #print(nouveau_elmts)
        return self.__class__(*nouveau_elmts) if len(nouveau_elmts) >= 2 else nouveau_elmts[0]

    def complementer(self):
        elements_complemente = [element.complementer() for element in list(self.elements)]

        nouveau_elmts = list(elements_complemente)
        for element in list(elements_complemente):
            if type(element) is Negatif:
                for element2 in list(elements_complemente):
                    if element2.est(element.element):
                        type_variable = Tautologie if self.__class__ is Or else Contradiction
                        nouveau_elmts.insert(nouveau_elmts.index(element), type_variable())
                        nouveau_elmts.remove(element)
                        nouveau_elmts.remove(element2)

        return self.__class__(*nouveau_elmts).idempotencer() \
               if len(nouveau_elmts) >= 2 else nouveau_elmts[0].idempotencer()

    def neutraliser(self):
        elements_neutralise = [element.neutraliser() for element in list(self.elements)]
        type_classe = Tautologie if self.__class__ is And else Contradiction
    
        elements_neutralise = [element for element in elements_neutralise \
                               if type(element) is not type_classe]

        return self.__class__(*elements_neutralise) \
               if len(elements_neutralise) >= 2 else elements_neutralise[0]

    def absorber(self):
        elements_absorbe = [element.absorber() for element in list(self.elements)]
        type_classe = Contradiction if self.__class__ is And else Tautologie
        if type_classe in [type(element) for element in elements_absorbe]:
            return type_classe()
        else:
            return self.__class__(*elements_absorbe)

    def associer(self):
        """ Associe les sous éléments à l'élément courant si cela est possible. """
        elements_associe = [element.associer() for element in list(self.elements)]

        nouveau_elmts = []
        for element in list(elements_associe):
            if type(element) is type(self):
                for element2 in element.elements:
                    nouveau_elmts.append(element2)
            else:
                nouveau_elmts.append(element)
        return self.__class__(*nouveau_elmts)

    def involuer(self):
        return self.__class__(*[element.involuer() for element in self.elements])

    def distribuer_or(self):
        nouveau = self.__class__(*[element.distribuer_or() for element in self.elements])
        return nouveau.associer()
    
    def distribuer_and(self):
        nouveau = self.__class__(*[element.distribuer_and() for element in self.elements])
        return nouveau.associer()

    def morganiser(self):
        return self.__class__(*[element.morganiser() for element in self.elements]).associer()

    def materialiser(self):
        return self.__class__(*[element.materialiser() for element in self.elements])

    def materialiser_double(self):
        return self.__class__(*[element.materialiser_double() for element in self.elements])

    def est(self, other):
        if self.__class__ is not other.__class__:
            return False
        if len(self.elements) != len(other.elements):
            return False
        for elmt in self.elements:
            present = False
            for elmt2 in other.elements:
                if elmt.est(elmt2):
                    present = True
            if not present:
                return False
        return True

    def rechercher_variables(self):
        variables = []
        for element in self.elements:
            for variable in element.rechercher_variables():
                if variable not in variables:
                    variables.append(variable)
        variables.sort()
        return variables

    def afficher_formule(self):
        symbole = " " + self.symbole + " "
        messages = []
        for elmt in self.elements:
            if isinstance(elmt, FormuleDeuxElement) or \
               isinstance(elmt, FormuleMultiElement):
                messages.append("(" + str(elmt) + ")")
            else:
                messages.append(str(elmt))
        return symbole.join(messages)


class Or(FormuleMultiElement):
    def __init__(self, *args):
        FormuleMultiElement.__init__(self, "˅", list(args))

    def distribuer_or(self):
        elmts = [element.distribuer_or() for element in self.elements]

        for element in elmts:
            if type(element) is And:
                if len(elmts) >= 3:
                    groupement = Or(*[elmt for elmt in elmts if elmt is not element])
                else:
                    groupement = [elmt for elmt in elmts if elmt is not element][0]

                return And(*[groupement + elmt for elmt in element.elements]).distribuer_or()

        return Or(*elmts)

    def calculer(self):
        null = False
        for element in self.elements:
            if element.calculer() == True:
                return True
            if element.calculer() is None:
                null = True
        return None if null else False


class And(FormuleMultiElement):
    def __init__(self, *args):
        FormuleMultiElement.__init__(self, "˄", list(args))

    def distribuer_and(self):
        elmts = [element.distribuer_and() for element in self.elements]

        for element in elmts:
            if type(element) is Or:
                if len(elmts) >= 3:
                    groupement = And(*[elmt for elmt in elmts if elmt is not element])
                else:
                    groupement = [elmt for elmt in elmts if elmt is not element][0]

                return Or(*[groupement * elmt for elmt in element.elements]).distribuer_and()

        return And(*elmts)

    def calculer(self):
        null = False
        for element in self.elements:
            if element.calculer() == False:
                return False
            if element.calculer() is None:
                null = True
        return None if null else True


class FormuleDeuxElement(Element):
    def __init__(self, symbole, element1, element2):
        assert isinstance(element1, Element), "L'élement 1 donné est mauvais : " + element1
        assert isinstance(element2, Element), "L'élément 2 donné est mauvais : " + element2
        Element.__init__(self)
        self.symbole = symbole
        self.element1 = element1
        self.element2 = element2
        self.variables = self.rechercher_variables()

    def idempotencer(self):
        return self.__class__(self.element1.idempotencer(), self.element2.idempotencer())

    def complementer(self):
        if self.element1.est(self.element2):
            return Tautologie()
        else:
            return self.__class__(self.element1.complementer(), self.element2.complementer())

    def associer(self):
        return self.__class__(self.element1.associer(), self.element2.associer())

    def involuer(self):
        return self.__class__(self.element1.involuer(), self.element2.involuer())

    def distribuer_and(self):
        return self.__class__(self.element1.distribuer_and(), self.element2.distribuer_and())

    def distribuer_or(self):
        return self.__class__(self.element1.distribuer_or(), self.element2.distribuer_or())

    def morganiser(self):
        return self.__class__(self.element1.morganiser(), self.element2.morganiser())

    def materialiser(self):
        return self.__class__(self.element1.materialiser(), self.element2.materialiser())

    def materialiser_double(self):
        element1 = self.element1.materialiser_double()
        element2 = self.element2.materialiser_double()
        return self.__class__(element1, element2)

    def rechercher_variables(self):
        variables = []
        for variable in self.element1.rechercher_variables():
            if variable not in variables:
                variables.append(variable)
        for variable in self.element2.rechercher_variables():
            if variable not in variables:
                variables.append(variable)
        variables.sort()
        return variables

    def afficher_formule(self):
        message = ""
        if isinstance(self.element1, FormuleDeuxElement) or \
           isinstance(self.element1, FormuleMultiElement):
            message += "(" + str(self.element1) + ")"
        else:
            message += str(self.element1)

        message += " " + self.symbole + " "

        if isinstance(self.element2, FormuleDeuxElement) or \
           isinstance(self.element2, FormuleMultiElement):
            message += "(" + str(self.element2) + ")"
        else:
            message += str(self.element2)
        return message


class Implication(FormuleDeuxElement):
    def __init__(self, element1, element2):
        FormuleDeuxElement.__init__(self, "⇒", element1, element2)

    def neutraliser(self):
        if type(self.element1) is Tautologie:
            return self.element2.neutraliser()
        if type(self.element2) is Contradiction:
            return -self.element1.neutraliser()
        return self.__class__(self.element1.neutraliser(), self.element2.neutraliser())

    def absorber(self):
        if type(self.element2) is Tautologie or type(self.element1) is Contradiction:
            return Tautologie()
        return self.__class__(self.element1.absorber(), self.element2.absorber())

    def materialiser(self):
        return (-self.element1 + self.element2).materialiser()

    def est(self, other):
        if self.__class__ is not other.__class__:
            return False
        return True if self.element1.est(other.element1) and self.element2.est(other.element2) \
               else False

    def calculer(self):
        if self.element1.calculer() == False:
            return True
        else:
            if self.element2.calculer():
                return True
            elif self.element2.calculer() == False:
                return False
            else:
                return None


class DoubleImplication(FormuleDeuxElement):
    def __init__(self, element1, element2):
        FormuleDeuxElement.__init__(self, "⇔", element1, element2)

    def neutraliser(self):
        if type(self.element1) is Tautologie:
            return self.element2
        if type(self.element2) is Tautologie:
            return self.element1
        if type(self.element1) is Contradiction:
            return -self.element2
        if type(self.element2) is Contradiction:
            return -self.element1
        return DoubleImplication(self.element1.neutraliser(), self.element2.neutraliser())

    def absorber(self):
        return DoubleImplication(self.element1.absorber(), self.element2.absorber())

    def materialiser_double(self):
        partie1 = self.element1 >> self.element2
        partie2 = self.element2 >> self.element1
        return (partie1 * partie2).materialiser_double()

    def est(self, other):
        if self.__class__ is not other.__class__:
            return False
        return True if (self.element1.est(other.element1) or self.element1.est(other.element2)) and \
               (self.element2.est(other.element1) or self.element2.est(other.element2)) \
               else False

    def calculer(self):
        if self.element1.calculer() is not None and self.element2.calculer() is not None:
            if self.element1.calculer() == self.element2.calculer():
                return True
            else:
                return False
        else:
            return None

















if __name__ == "__main__":
    taut, cont = Tautologie(), Contradiction()
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = [Variable(lettre) for lettre in "abcdefghijklmnopqrstuvwxyz"]
    
    f1 = (((c >> ((b + a) * d)) * (b % (a * (c + d))) * (c >> a)) + ((b * a) >> d))


    f2 = -((x >> w) >> ((y >> z) >> ((x + y) >> (w * y * z * -x))))


    f3 = p * (-p + -q + r) * q * (-u + v) * (-p + -r + t) * (-q + -t + s) * (-u + -r + t)


    f1.normaliser()

    

