

temps_recolte = 30 * 60

class fourmi:
    def __init__(self, nom, vie, attaque, defense, temps, nourriture):
        self.nom = nom

        self.vie = vie
        self.attaque = attaque
        self.defense = defense
        
        self.temps = temps
        self.nourriture = nourriture

        self.afficher_stat()

    def afficher_stat(self):
        print(self.nom)
        nombre_par_recolte = temps_recolte / self.temps
        print("Nombre pour une récolte :", nombre_par_recolte)
        vie_par_recolte = self.vie * nombre_par_recolte
        print("Vie totale :", vie_par_recolte)
        attaque_par_recolte = self.attaque * nombre_par_recolte
        print("Attaque totale :", attaque_par_recolte)
        defense_par_recolte = self.defense * nombre_par_recolte
        print("Defense totale :", defense_par_recolte)
        nourriture_par_recolte = self.nourriture * nombre_par_recolte
        print("Nourriture totale :", nourriture_par_recolte)

        print("-"*50)



jsn = fourmi("Jeune soldate naine", 8, 3, 2, 22, 16)
sn = fourmi("Soldate naine", 10, 5, 4, 32, 20)
ne = fourmi("Naine d'élite", 13, 7, 6, 41, 26)
js = fourmi("Jeune soldate", 16, 10, 9, 53, 30)
s = fourmi("Soldate", 20, 15, 14, 72, 36)
c = fourmi("Concierge", 30, 1, 25, 101, 70)
a = fourmi("Artilleuse",10, 30, 15, 103, 30)
ae = fourmi("Artilleuse d'élite", 12, 35, 18, 109, 34)
se = fourmi("Soldate d'élite", 72, 24, 23, 104, 44)
t = fourmi("Tank", 35, 55, 1, 134, 100)
tu = fourmi("Tueuse", 50, 50, 50, 197, 80)
tue = fourmi("Tueuse d'élite", 55, 55, 55, 197, 90)
