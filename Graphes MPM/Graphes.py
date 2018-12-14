
# Générateur de graphe MPM

from math import inf

taches = []

class Tache:
    def __init__(self, nom, duree, *predecesseurs):
        taches.append(self)
        # Propriétés
        self.nom = nom
        self.duree = duree
        self.predecesseurs = list(predecesseurs)
        # Anti transitivité.
        for p1 in list(self.predecesseurs):
            for p2 in list(self.predecesseurs):
                if p1 is not p2:
                    if p1.recherche_predecesseur(p2):
                        self.predecesseurs.remove(p2)
                        print("/!\ Une tâche a été retiré : ", p2)

        # Liaisons.
        self.successeurs = []
        for predecesseur in self.predecesseurs:
            predecesseur.successeurs.append(self)

        # Date au plus tôt et date au plus tard.
        self.date_plus_tot = None
        self.date_plus_tard = None

    def recherche_predecesseur(self, tache):
        if tache is self:
            return True
        else:
            for p in self.predecesseurs:
                resultat = p.recherche_predecesseur(tache)
                if resultat:
                    return resultat
        return False

    def recherche_successeur(self, tache):
        if tache is self:
            return True
        else:
            for p in self.successeurs:
                resultat = p.recherche_successeur(tache)
                if resultat:
                    return resultat
        return False

    def calculer_date_au_plus_tot(self):
        maximum = -inf
        for p in self.predecesseurs:
            if p.date_plus_tot == None:
                p.calculer_date_au_plus_tot()
            maximum = max(maximum, p.date_plus_tot + p.duree)
        self.date_plus_tot = maximum

    def calculer_date_au_plus_tard(self):
        minimum = inf
        for s in self.successeurs:
            if s.date_plus_tard == None:
                s.calculer_date_au_plus_tard()
            minimum = min(minimum, s.date_plus_tard - self.duree)
        self.date_plus_tard = minimum

    def calculer_chemin_critique(self, chemin):
        assert self.date_plus_tot is not None,"La date au plus tot doit d'abord etre calculer"
        assert self.date_plus_tard is not None,"La date au plus tard doit d'abord etre calculer"
        if self.date_plus_tot != self.date_plus_tard:
            return None
        else:
            chemin.append(self)
            for p in self.predecesseurs:
                un_chemin = p.calculer_chemin_critique(chemin)
                if un_chemin is not None:
                    chemin = un_chemin
            return chemin

    def listage_predecesseurs(self, predecesseurs=[]):
        """ Retourne une liste de tout les prédécesseurs profond de la tâche. """
        mes_predecesseurs = list(predecesseurs)
        for p in self.predecesseurs:
            mes_predecesseurs = p.listage_predecesseurs(mes_predecesseurs)
        if self not in mes_predecesseurs:
            mes_predecesseurs.append(self)
        
        return mes_predecesseurs

    def volume(self):
        """ Calcule le volume en faisant la somme de la durée de tout les prédécesseurs """
        return sum([p.duree for p in self.listage_predecesseurs()])


    def affichage_tableau(self):
        return self.nom + " (" + str(self.duree) + ") " + str(self.date_plus_tot) + "/" + str(self.date_plus_tard)

    def dot(self):
        texte = '"{}"'.format(self.nom)
        if len(self.successeurs):
            texte += " -> "
        successeurs = ['"{}"'.format(successeur.nom) for successeur in self.successeurs]
        texte += ", ".join(successeurs)
        return texte

    def __str__(self):
        p = [str(t.nom) for t in self.predecesseurs]
        p = ", ".join(p)
        return self.nom + " (" + str(self.duree) + ")" + " [" + p + "]"

    def __repr__(self):
        return self.nom


class Graphe:
    def __init__(self, *taches):
        self.debut = Tache("Début", 0)
        self.fin = Tache("Fin", 0)
        self.taches = list(taches)
        # Relier début et fin.
        for t in self.taches:
            if t.predecesseurs == []:
                t.predecesseurs.append(self.debut)
                self.debut.successeurs.append(t)
            if t.successeurs == []:
                t.successeurs.append(self.fin)
                self.fin.predecesseurs.append(t)

        # Date au plus tôt et date au plus tard.
        self.debut.date_plus_tot = 0
        self.fin.calculer_date_au_plus_tot()
        self.fin.date_plus_tard = self.fin.date_plus_tot
        self.debut.calculer_date_au_plus_tard()

        self.chemin_critique = self.fin.calculer_chemin_critique([])

    def volume(self):
        return self.fin.volume()

    def affichage_tableau(self):
        textes = ["Nom | Durée | Date au plus tôt/Date au plus tard"]
        for t in self.taches:
            textes.append(t.affichage_tableau())
        textes.append(self.fin.affichage_tableau())
        return "\n".join(textes)

    def dot(self):
        texte = """digraph Gphe {\n"""
        texte += "\t" + self.debut.dot() + ";\n"
        for tache in self.taches:
            texte += "\t" + tache.dot() + ";\n"
        texte += "}"
        return texte














if __name__ == "__main__":
    A = Tache("Ma première tâche", 5)
    B = Tache("Ma deuxième tâche", 2, A)
    C = Tache("Une troisième tâche", 2, A, B)
    Gphe = Graphe(A, B, C)

