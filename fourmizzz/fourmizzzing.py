
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
        if "h" in texte or "H" in texte:
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
    equivalent = {"Ouvriere":"ouvriere",
                  "Jeune Soldate Naine":"unite1",
                  "Soldate Naine":"unite2",
                  "Naine d'élite":"unite3",
                  "Jeune Soldate":"unite4",
                  "Soldate":"unite5",
                  "Concierge":"unite6",
                  "Artilleuse":"unite7",
                  "Artilleuse d'élite":"unite8",
                  "Soldate d'élite":"unite9",
                  "Tank":"unite10",
                  "Tueuse":"unite11",
                  "Tueuse d'élite":"unite12"}

    def __init__(self):
        self.browser = RoboBrowser(user_agent="Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0")
        self.connexion()

        # Ressources.
        self.ouvrieres = 0
        self.nourriture = 0
        self.bois = 0
        self.tdc = 0
        self.get_ressource()

        # Armées.
        self.armee = {}
        self.get_armee()

        # Chasse.
        self.temps_chasse = timedelta()
        self.get_temps_chasse()

        # Production.
        self.production = 0

        # Affichage.
        self.nbr_boucle = 0

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
        self.page("Armée")

        divs = self.browser.find_all("div", {"class":"pas_sur_telephone"})
        unites = [div.text for div in divs]
        for unite in unites:
            titre = self.browser.find("div", text=unite)
            p = titre.parent.parent
            self.armee[unite] = 0
            for nb in p.findAll("span"):
                self.armee[unite] += int(nb.text.replace(" ", ""))

    def armee_totale(self):
        """ Retourne le nombre d'unité totale. """
        nbr = 0
        for key, item in self.armee.items():
            nbr += item
        return nbr

    def get_temps_chasse(self):
        """ Recueil le temps de chasse restant. """
        self.page("Ressources")

        span = self.browser.find_all("span", {"class":"titre"})[-1]
        if span.text != "Chasse en cours ":
            self.temps_chasse = timedelta()
            return False

        temps = span.next_sibling()[0].text
        self.temps_chasse = parser_temps(temps)

    def page(self, nom_page):
        """ Permet d'acceder à une page par son nom. """
        while True:
            erreur = False
            link = self.browser.get_link(nom_page)
            if link is not None:
                try: self.browser.follow_link(link)
                except ConnectionError: erreur = True
            alerte = self.browser.find("script", text="""alert("Vous venez de vous connecter avec un second navigateur ou quelqu'un vient de se connecter sur votre compte. Il est conseillé de vous reconnecter et de changer votre mot de passe.");""")
            if alerte is not None:
                erreur = True
            if not erreur:
                break
            self.connexion()

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

    def cm2_chassable(self, *types_unite):
        """ Retourne le nombre de cm2 conquerable selon les unités donnée. """
        self.get_armee()
        cm2 = 0
        for unite in types_unite:
            cm2 += int(self.armee[unite] * 0.03)
        return cm2

    def chasser(self, *types_unite):
        """ Permet de chasser proportionnelement à la taille de l'unité qui va chasser. """
        cm2 = self.cm2_chassable(*types_unite)
        if not cm2:
            return False

        # Remplir le formulaire avec le nombre de cm2 à chasser.
        self.page("Ressources")

        form = self.browser.get_form(action="AcquerirTerrain.php")
        if form is None:
            print("Erreur form")
            return False
        form["AcquerirTerrain"] = cm2
        self.browser.submit_form(form)

        # Mettre les arméees inutiles à 0.
        form = self.browser.get_form(action="AcquerirTerrain.php")
        for cle, item in Fourmilliere.equivalent.items():
            if cle in types_unite:
                if form[item] == 0:
                    print("Erreur unité")
                    return False
            else:
                try: form[item] = 0
                except: pass

        self.browser.submit_form(form)

        self.get_temps_chasse()

        return True

    def pondre(self, type_unite, pourcent):
        """ Permet de faire pondre la reine. Le pourcent correspond au temps de chasse. """
        self.get_temps_chasse()

        self.page("Reine")

        # Calcul temps.
        type_unite = Fourmilliere.equivalent[type_unite]
        input_unite = self.browser.find("input", {"value":type_unite})
        tr = input_unite.parent.parent
        spans = tr.findAll("span", {"style":"height:20px;width:85px;display:inline-block;"})
        temps_unite = parser_temps(spans[0].text)
        nourriture_unite = int(spans[1].text.replace(" ", ""))

        temps_possible = self.temps_chasse * pourcent
        nombre = int(temps_possible / temps_unite)
        quotien = timedelta(minutes=30) / self.temps_chasse
        self.production += int(nourriture_unite * nombre * quotien)

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
        print(self)
        while True:
            try:
                self.connexion()
                self.boucle_chasse()
                self.boucle_amelioration()
                dormir(60)
            except:
                dormir(5)

    def boucle_chasse(self):
        # Regarder combien de temps avant la prochaine chasse..
        try:
            self.get_temps_chasse()
            temps_restant = int(self.temps_chasse.seconds / 60)
            if not temps_restant:
                self.get_ressource()
                self.get_armee()
                print(str(self) + " (" + str(self.nbr_boucle) + ")" )
            else:
                print(str(temps_restant), end=" ")

            # Début.
            self.production = 0
            if self.chasser("Jeune Soldate", "Artilleuse"):
                self.pondre("Ouvriere", 0.3)
                self.pondre("Jeune Soldate Naine", 0.1)
                self.pondre("Concierge", 0.1)
                self.pondre("Jeune Soldate", 0.25)
                self.pondre("Artilleuse", 0.25)

                self.faire_travailler()

                self.nbr_boucle += 1
        except Exception as e:
            print(e)
            pass

    def boucle_amelioration(self):
        try:
            self.construire("Champignonnière")
            self.construire("Entrepôt de Nourriture")
            self.construire("Entrepôt de Matériaux")
            self.construire("Couveuse")
            self.construire("Solarium")
            self.construire("Laboratoire")
            self.construire("Salle d'analyse")
            self.construire("Etable à cochenilles")

            self.rechercher("Technique de ponte")
            self.rechercher("Bouclier Thoracique")
            self.rechercher("Armes")
            self.rechercher("Architecture")
            self.rechercher("Communication avec les animaux")
            self.rechercher("Vitesse de chasse")
        except:
            print("Erreur amélioration.")

    def __str__(self):
        text = "{0} nourriture, {1} materiaux, {2} ouvrieres, {3} tdc, {4} unités.".format(self.nourriture, self.bois, self.ouvrieres, self.tdc, self.armee_totale())
        return text


if __name__ == "__main__":
    while True:
        try:
            f = Fourmilliere()
            break
        except:
            pass
    f.boucle()

    pass
