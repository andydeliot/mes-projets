
# Générateur de graphe MPM

from math import inf

taches = []

class Tache:
    """ Aussi appelé étape. Représente une action à réaliser. """
    def __init__(self, nom, duree, *predecesseurs):
        """ Testé. """
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
        """ Testé. Renvoi vrai si tache est un prédécésseur. """
        if tache is self:
            return True
        else:
            for p in self.predecesseurs:
                resultat = p.recherche_predecesseur(tache)
                if resultat:
                    return resultat
        return False

    def recherche_successeur(self, tache):
        """ Testé. Renvoi vrai si tache est un successeur. """
        if tache is self:
            return True
        else:
            for p in self.successeurs:
                resultat = p.recherche_successeur(tache)
                if resultat:
                    return resultat
        return False

    def calculer_date_au_plus_tot(self):
        """ Testé. Procédure récursive donnant la date au plus tôt de la tâche. """
        maximum = -inf
        for p in self.predecesseurs:
            if p.date_plus_tot == None:
                p.calculer_date_au_plus_tot()
            maximum = max(maximum, p.date_plus_tot + p.duree)
        self.date_plus_tot = maximum

    def calculer_date_au_plus_tard(self):
        """ Testé. Procédure récursive donnant la date au plus tard de la tâche. """
        minimum = inf
        for s in self.successeurs:
            if s.date_plus_tard == None:
                s.calculer_date_au_plus_tard()
            minimum = min(minimum, s.date_plus_tard - self.duree)
        self.date_plus_tard = minimum

    def calculer_chemin_critique(self, chemin):
        """ Testé mais non fonctionnel. Renvoi une liste contenant le chemin critique.
            L'algorithme ne fonctionne pas s'il existe plusieurs chemin critique. """
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
        """ Testé. Retourne une liste de tout les prédécesseurs profond de la tâche. """
        mes_predecesseurs = list(predecesseurs)
        for p in self.predecesseurs:
            mes_predecesseurs = p.listage_predecesseurs(mes_predecesseurs)
        if self not in mes_predecesseurs:
            mes_predecesseurs.append(self)
        
        return mes_predecesseurs

    def volume(self):
        """ Testé. Calcule le volume.
            C'est à dire, la somme de la durée de tout les prédécesseurs """
        return sum([p.duree for p in self.listage_predecesseurs()])

##    def calcul_marge(self):
##        """ Fonction non testé. Permet de calculer la marge libre de la tâche. """
##        assert self.date_plus_tot is not None, "Calculez d'abord la date au plus tôt"
##        assert self.date_plus_tard is not None, "Calculez d'abord la date au plus tard"
##        return date_plus_tard - date_plus_tot

    def affichage_tableau(self):
        """ Testé. Renvoie une string pour un meilleur affichage. """
        return self.nom + " (" + str(self.duree) + ") " + str(self.date_plus_tot) + "/" + str(self.date_plus_tard)

    def dot(self):
        """ Testé. Renvoi un texte dot de la tâche pour l'affichage dans GraphViz. """
        couleur = '\t"{}"'.format(self.nom)
        if self.date_plus_tot == self.date_plus_tard:
            couleur += " [color=red, style=filled]"
        couleur += ';\n'
        texte = '\t"{}"'.format(self.nom)
        if len(self.successeurs):
            texte += " -> "
        successeurs = ['"{}"'.format(successeur.nom) for successeur in self.successeurs]
        texte += ", ".join(successeurs)
        texte += ";\n"
        return couleur + texte

    def generation_html(self, taille_totale=0):
        """ Testé. Renvoi une string représentant l'étape dans une ligne html.
            Taille totale représente la taille du tableau (en durée).
            Elle est de zéro si la tâche ne se trouve pas dans un graphe. """
        date_plus_tot = self.date_plus_tot if self.date_plus_tot is not None else 0
        date_plus_tard = self.date_plus_tard if self.date_plus_tard is not None else 0
        debut = "<td>" * date_plus_tot
        duree = '<td bgcolor="#FF5733">' * self.duree
        marge = '<td bgcolor="#3375FF">' * (date_plus_tard - date_plus_tot)
        fin = "<td>" * (taille_totale - date_plus_tard - self.duree)
        texte = "<tr height=40><td>{}</td>{}{}{}{}</tr>\n".format(self.nom, debut, duree, marge, fin)
        return texte

    def __str__(self):
        p = [str(t.nom) for t in self.predecesseurs]
        p = ", ".join(p)
        return self.nom + " (" + str(self.duree) + ")" + " [" + p + "]"

    def __repr__(self):
        return self.nom


class Graphe:
    """ Représente un ensemble de taches. """
    def __init__(self, *taches):
        """ Testé. """
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
        """ Testé. Calcule le volume du graphe.
            C'est à dire, la somme de la durée de toutes les étapes du graphe."""
        return self.fin.volume()

    def affichage_tableau(self):
        """ Testé. Affiche les taches dans un tableau. """
        textes = ["Nom | Durée | Date au plus tôt/Date au plus tard"]
        for t in self.taches:
            textes.append(t.affichage_tableau())
        textes.append(self.fin.affichage_tableau())
        return "\n".join(textes)

    def dot(self):
        """ Testé. Renvoi un texte dot du graphe pour l'affichage dans GraphViz. """
        texte = """digraph Gphe {\n"""
        texte += self.debut.dot()
        for tache in self.taches:
            texte += tache.dot()
        texte += '\t"{}" [color=red, style=filled];\n'.format(self.fin.nom)
        texte += "}"
        return texte

    def generation_html(self):
        """ Testé. Génère le html du graphe sous forme de string. """
        texte = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
        texte += '<table width="{}" border=5>\n'.format(self.fin.date_plus_tot*20+1000)
        texte += "<tr><th>Nom de l'étape</th>"
        texte += "".join(["<th width=20>{}</th>".format(i) for i in range(0, self.fin.date_plus_tot)])
        texte += "</tr>\n"
        for tache in self.taches:
            texte += tache.generation_html(self.fin.date_plus_tot)
        texte += "</table>\n"
        return texte












if __name__ == "__main__":
    A = Tache("Ma première tâche", 5)
    B = Tache("Ma deuxième tâche", 2, A)
    C = Tache("Une troisième tâche", 2, A, B)
    Gphe = Graphe(A, B, C)

