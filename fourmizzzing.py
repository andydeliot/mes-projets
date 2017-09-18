
import time
import arrow
from datetime import timedelta
from robobrowser import RoboBrowser


def parser_temps(texte_temps):
    textes = texte_temps.split(" ")
    secondes = 0
    minutes = 0
    heures = 0
    for texte in textes:
        if "s" in texte:
            texte = texte[:-1]
            texte = texte.split(".")[0]
            secondes = int(texte)
        if "m" in texte:
            texte = texte[:-1]
            texte = texte.split(".")[0]
            minutes = int(texte)
        if "h" in texte:
            texte = texte[:-1]
            texte = texte.split(".")[0]
            heures = int(texte)
    return timedelta(hours=heures, minutes=minutes, seconds=secondes)

def dormir(temps):
    if type(temps) is int:
        time1 = time.time()
        while True:
            if time.time() - time1 >= temps:
                break
    if type(temps) is arrow.Arrow:
        while True:
            if arrow.utcnow() > temps:
                break


class Fourmilliere:
    nourriture_unite = {"ouvriere":5,
                        "unite1":16,
                        "unite2":20,
                        "unite3":26,
                        "unite4":30,
                        "unite5":36,
                        "unite6":70,}
    def __init__(self):
        self.browser = RoboBrowser(user_agent="Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0")
        self.connexion()
        
        self.ouvrieres = 0
        self.nourriture = 0
        self.bois = 0
        self.tdc = 0

        self.get_ressource()

        self.armee = 0
        self.get_armee()
        
        self.temps_chasse = timedelta()
        self.get_temps_chasse()

        self.production = 0

    def connexion(self):
        """ Connexion avec nom d'utilisateur et mdp. """
        url = "http://s4.fourmizzz.fr/Reine.php"
        self.browser.open(url)

        try:
            form = self.browser.get_form(id="loginForm")
            form["pseudo"] = "AdrenalineChallenger"
            form["mot_passe"] = "p3Ace70v3zzz"

            self.browser.submit_form(form)
            print("Connecté.")
        except:
            pass

    def get_ressource(self):
        """ Recueil les ressources de bases du jeu. """
        self.ouvrieres = int(self.browser.find(id="nb_ouvrieres").text)
        self.nourriture = int(self.browser.find(id="nb_nourriture").text.split(".")[0])
        self.bois = int(self.browser.find(id="nb_materiaux").text)
        self.tdc = int(self.browser.find(id="quantite_tdc").text)

    def get_armee(self):
        """ Recueil le nombre d'armée totale. """
        self.page("Armée")

        total = 0
        for unite in ["Jeune Soldate",
                      "Soldate",
                      "Soldate d’élite"]:
            titre = self.browser.find("div", text=unite)
            p = titre.parent.parent
            for u in p.findAll("span"):
                total += int(u.text.replace(" ", ""))

        self.armee = total

    def get_temps_chasse(self):
        """ Recueil le temps de chasse restant. """
        self.page("Ressources")

        span = self.browser.find_all("span", {"class":"titre"})[-1]
        if span.text != "Chasse en cours ":
            self.temps_chasse = timedelta()
            return False

        temps = span.next_sibling()[0].text
        self.temps_chasse = parser_temps(temps) + timedelta(minutes=1, seconds=30)

    def page(self, nom_page):
        """ Permet d'acceder à une page par son nom. """
        while True:
            link = self.browser.get_link(nom_page)
            if link is not None:
                self.browser.follow_link(link)
            erreur = self.browser.find("script", text="""alert("Vous venez de vous connecter avec un second navigateur ou quelqu'un vient de se connecter sur votre compte. Il est conseillé de vous reconnecter et de changer votre mot de passe.");""")
            if erreur is not None:
                self.connexion()
            else:
                break

    def faire_travailler(self):
        """ Fais partager les travailleuses entre les deux ressources possibles. """
        self.page("Ressources")

        self.get_ressource()

        ouvrieres = self.tdc if self.tdc < self.ouvrieres else self.ouvrieres
        nourriture = self.production if self.production < ouvrieres else ouvrieres
        materiaux = ouvrieres - nourriture
        
        form = self.browser.get_form(action="Ressources.php")
        form["RecolteNourriture"] = nourriture
        form["RecolteMateriaux"] = materiaux
        self.browser.submit_form(form)

    def chasser(self):
        """ Permet de chasser proportionnelement à la taille de l'armée. Récupère le temps de chasse. """
        self.get_armee()
        cm2 = int(self.armee * 0.03)
        if cm2 == 0:
            return False

        self.page("Ressources")

        form = self.browser.get_form(action="AcquerirTerrain.php")
        if form is None:
            return False
        form["AcquerirTerrain"] = cm2
        self.browser.submit_form(form)

        form = self.browser.get_form(action="AcquerirTerrain.php")
        try: form["unite1"] = 0
        except: pass
        try: form["unite2"] = 0
        except: pass
        try: form["unite3"] = 0
        except: pass
        if form["unite4"] == 0:
            return False
        self.browser.submit_form(form)

        self.get_temps_chasse()

        return True

    def pondre(self, type_unite, pourcent):
        """ Permet de faire pondre la reine. Le pourcent correspond au temps de chasse. """
        self.get_temps_chasse()

        self.page("Reine")

        # Calcul temps.
        input_unite = self.browser.find("input", {"value":type_unite})
        tr = input_unite.parent.parent
        span = tr.find("span", {"style":"height:20px;width:85px;display:inline-block;"})
        temps_unite = parser_temps(span.text)

        temps_possible = self.temps_chasse * pourcent
        nombre = int(temps_possible / temps_unite)
        quotien = timedelta(minutes=30) / self.temps_chasse
        self.production += Fourmilliere.nourriture_unite[type_unite] * nombre * quotien

        form = self.browser.get_form(action="Reine.php")
        form["typeUnite"] = type_unite
        form["nombre_de_ponte"] = nombre

        self.browser.submit_form(form)

    def construire(self, batiment):
        """ Cherche à construire un batiment particulier. """
        self.page("Construction")

        h2 = self.browser.find("h2", text=batiment)
        tr = h2.parent.parent
        div = tr.find("div", {"class":"icone_construction"})
        if div is not None:
            link = div.find("a")
            self.browser.follow_link(link)
            print(str(batiment) + " construit.")

    def rechercher(self, amelioration):
        """ Cherche à rechercher une amélioration particuliere. """
        self.page("Laboratoire")
        self.get_ressource()

        # Nombre d'ouvrieres nécéssaire.
        h2 = self.browser.find("h2", text=amelioration)
        tr = h2.parent.parent
        div = tr.find("div", {"class":"ouvriere"})
        ouvrieres_necessaire = int(div.text.replace(" ", ""))

        if self.ouvrieres - ouvrieres_necessaire < self.tdc and ouvrieres_necessaire > 0:
            return False

        div = tr.find("div", {"class":"icone_recherche"})
        if div is not None:
            link = div.find("a")
            self.browser.follow_link(link)
            print(str(amelioration) + " recherché.")

    def boucle(self):
        """ Tourne le programme en boucle. """
        nbr_boucle = 0
        print(str(self) + "------ " + str(nbr_boucle))
        while True:
            self.connexion()
            # Attente.
            print("Il reste : ", end='')
            while True:
                self.get_temps_chasse()
                a = int(self.temps_chasse.seconds / 60)
                if a == 0:
                    break
                print(str(a)+", ", end='')
                dormir(60)
            print("0 !")
            self.get_ressource()
            print(str(self) + "------ " + str(nbr_boucle))
            # Début.
            self.production = 100
            # Chasse.
            if self.chasser():
                # Ponte.
                self.pondre("ouvriere", 0.3)
                self.pondre("unite1", 0.2)
                self.pondre("unite4", 0.5)
            # Travail. 
            self.faire_travailler()
            # Construction et amélioration.
            self.construire("Laboratoire")
            self.rechercher("Armes")
            self.rechercher("Bouclier Thoracique")
            self.rechercher("Vitesse de chasse")
            self.rechercher("Technique de ponte")
            self.construire("Couveuse")
            self.construire("Solarium")
            self.construire("Entrepôt de Matériaux")
            self.rechercher("Architecture")
            self.rechercher("Vitesse d'attaque")

            nbr_boucle += 1

    def __str__(self):
        text = "{0} nourriture, {1} materiaux, {2} ouvrieres, {3} tdc.".format(self.nourriture, self.bois, self.ouvrieres, self.tdc)
        return text


# Récupérer les informations.

f = Fourmilliere()

if __name__ == "__main__":
    f.boucle()

    pass

