
from random import randrange, randint, choice
from statistics import mean
from numpy import corrcoef
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


VALEUR_TRAVAIL = 15
COEF_VALEUR_QUALIFICATION = 1.2

class Employer:
    def __init__(self, qualification):
        self.qualification = qualification
        self.demandes = []

    def valeur_travaille(self, heures):
        """ Retourne la valeur du travail de l'employer. """
        return heures * (1 + COEF_VALEUR_QUALIFICATION * self.qualification) * VALEUR_TRAVAIL

    def salaire(self, salaire_qualification):
        """ Retourne le salaire final de l'employer. """
        return salaire_qualification * (1 + self.qualification)

    def demande(self, entreprise):
        """ Ajoute une demande d'embouche. """
        self.demandes.append(entreprise)

    def prendre_demande(self):
        """ Rentre dans une entreprise. """
        demandes = sorted(self.demandes, key = lambda x: x.horaire / x.salaire_qualification)
        try:
            demandes[0].prendre(self)
        except:
            pass

    def __str__(self):
        return "({0})".format(self.qualification)

class Entreprise:
    def __init__(self, horaire, salaire_qualification):
        self.horaire = horaire
        self.salaire_qualification = salaire_qualification
        self.employes = []

    def prendre(self, employer):
        """ Emploie un employer. """
        self.employes.append(employer)

    def benefice(self):
        """ Retourne le bénéfice de l'entreprise. """
        valeurs = sum([employer.valeur_travaille(self.horaire) for employer in self.employes])
        salaires = sum([employer.salaire(self.salaire_qualification) for employer in self.employes])
        return valeurs - salaires

    def benefice_par_employer(self):
        """ Retourne le bénéfice par employés. """
        return self.benefice() / len(self.employes)

    # Statistiques.
    def niveau_moyen(self):
        """ Retourne le niveau de qualification moyen de l'entreprise. """
        return mean([employer.qualification for employer in self.employes])

    def __str__(self):
        msg = "{0}h; {1}€/lvl; {2}lvl; {3}w; {5}€/w; {4}€;".format(self.horaire, self.salaire_qualification, round(self.niveau_moyen(), 2), len(self.employes),
                                                                        round(self.benefice_par_employer()), self.benefice() )
        return msg


class Ville:
    def __init__(self, population, nbr_entreprise):
        self.habitants = [Employer(randrange(5)) for _ in range(population)]
        self.entreprises = [Entreprise(randint(1500, 5000)/100*4, 1000) for _ in range(nbr_entreprise)]

        for e in self.entreprises:
            demandes = sorted([choice(self.habitants) for _ in range(int(population*0.01))], key=lambda x: x.qualification, reverse=True)
            for d in demandes:
                d.demande(e)

        for h in self.habitants:
            h.prendre_demande()

        self.entreprises = [e for e in self.entreprises if len(e.employes) > 0 and e.benefice() > 0]
        self.entreprises = sorted(self.entreprises, key=lambda x: x.benefice())
        for e in self.entreprises:
            print(e)

        print(self.benef_par_tranche_horaire())
        
    def benef_par_tranche_horaire(self):
        """ Retourne le bénéfice moyen selon les différents horaires disponibles. """
        x = [e.horaire for e in self.entreprises]
        y = [e.benefice() for e in self.entreprises]
        z = [len(e.employes) for e in self.entreprises]
        fig = pyplot.figure()
        Axes3D(fig).scatter(x, y, z)
        pyplot.show()
        return corrcoef(x, y)[1, 0]



st_foy = Ville(10000, 2000)


























