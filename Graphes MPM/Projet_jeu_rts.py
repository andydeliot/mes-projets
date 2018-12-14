
# Création du graphe MPM pour le projet de jeu rts


import os

from Graphes import Tache, Graphe, taches


# Icones.
Icones_unite = Tache("Dessiner plusieurs icones pour représenter les 5 différentes unités", 3)
Icone_batiment = Tache("Dessiner les icones des 3 différents batiments", 2)
Icone_creation_unite = Tache("Dessiner l'icone de création des unitées", 1)
Icone_creation_batiment = Tache("Dessiner l'icone de construction de batiment", 2)

Icone_mouvement = Tache("Dessiner l'icone de mouvement des unitées", 1)
Icone_attaque_deplacement = Tache("Dessiner l'icone d'attaque-déplacement des unitées", 1)
Icone_garde = Tache("Dessiner l'icone de garde des unitées", 1)

# Modélisations.
Modeliser_unite = Tache("Modeliser une unité", 1)
Modeliser_autre_unite = Tache("Modélisation des 4 autres unitées", 4)
Modeliser_projectile = Tache("Modeliser un projectile", 1)
Modeliser_batiment_principal = Tache("Modeliser le batiment principal", 2)
Modeliser_autre_batiment = Tache("Modélisation des 2 autres batiments", 2)


# Absolument nécéssaire.
Unreal = Tache("Créer un projet unreal engine", 1)

# Gameplay.
Camera = Tache("Créer une camera movible", 3, Unreal)
Ajout_argent = Tache("Ajout du gameplay et de l'HUD de l'argent pour les joueurs", 2, Unreal)
Ajout_population = Tache("Ajout du gameplay et de l'HUD de la population pour les joueurs", 2, Unreal)

# Unité.
Creer_unite = Tache("Créer une unité c'est-à-dire le blueprint les propriétés d'attaque de défense la vitesse la taille la population l'argent etc", 1, Unreal, Modeliser_unite)
Creer_unite_ennemi = Tache("Créer une unité ennemi donc rajouter la notion d'équipe", 1, Modeliser_unite)
Selection = Tache("Selectionner et deselectionner une unité", 2, Creer_unite, Creer_unite_ennemi) # une unité ennemi est nécéssaire pour faire une vrai selection.
Selection_multiple = Tache("Selectionner plusieurs unités et les déplacer en même temps", 2, Selection)
PV_unite = Tache("Afficher les points de vie des unitées", 2, Creer_unite)
HUD_unite = Tache("Créer le HUD de l'unité lorsque celle-ci est sélectionné", 2, Selection)

# Ordre unité.
Rotation_unite = Tache("Faire pivoter l'unité selectionné dans la direction du clic", 3, Selection, Icone_mouvement, HUD_unite)
Mouvement_unite = Tache("Faire bouger l'unité selectionné jusqu'à la position du clic", 3, Rotation_unite)
Collision_unite = Tache("Gérer les collisions des unitées", 5, Mouvement_unite, Creer_unite, Creer_unite_ennemi)
Attaque_unite = Tache("Faire attaquer une unité et enlever des pvs", 3, Selection, Creer_unite_ennemi, PV_unite, Modeliser_projectile, Icone_attaque_deplacement, HUD_unite)
Attaque_deplacement = Tache("Créer une action permettant de faire attaquer-déplacer une unité", 2, Attaque_unite, Mouvement_unite, Icone_attaque_deplacement)
Garde_unite = Tache("Créer une action permettant d'immobiliser une unité et la faire attaquer à vue", 1, Selection, Icone_garde, HUD_unite)
Mort_unite = Tache("Faire mourir les unitées", 2, Attaque_unite)


# Interface.
Menu_jeu = Tache("Créer le menu du jeu", 1, Unreal)
Interface_creation_unite = Tache("Créer l'interface de la création des unitées hors combats", 2, Unreal)
Generation_unite = Tache("Générer le blueprint des unités inventé en dehors des combats avec les dégats l'argent la population etc", 4, Interface_creation_unite)
Interface_creation_batiment = Tache("Créer l'interface de la création des batiments hors combats", 2, Unreal)
Generation_batiment = Tache("Générer le blueprint des batiments inventé hors combats avec les capacités la population l'argent etc", 3, Interface_creation_batiment)
Interface_creation_equipe = Tache("Créer l'interface de la création de son équipe avec la liste des unités et des batiments", 2, Menu_jeu, Icones_unite)
Interface_connexion = Tache("Créer l'interface de connexion pour le jeu en réseau", 2, Unreal)


# Batiment.
Creer_batiment_principal = Tache("Créer le batiment principal", 1, Modeliser_batiment_principal, Unreal)
PV_batiment = Tache("Afficher les points de vie des batiments", 1, Creer_batiment_principal)
Destruction_batiment = Tache("Faire se détruire les batiments", 2, PV_batiment)
Creation_batiment_action = Tache("Ajouter des actions au batiment durant la création de batiment hors combat", 3, Ajout_argent, Ajout_population, Interface_creation_batiment)

# Ordre batiment.
HUD_batiment = Tache("Créer le HUD du batiment lorsque celui-ci est sélectionné", 2, Creer_batiment_principal, Selection)
Batiment_creation_unite = Tache("Création d'unitées par le batiment", 3, Icone_creation_unite, Icones_unite, HUD_batiment)
Construction_batiment = Tache("Construction de batiment par les batiments", 3, Icone_creation_batiment, Icone_batiment, HUD_batiment, Modeliser_autre_batiment, Camera)
Empecher_chevauchement_batiment = Tache("Empecher que deux batiments soient construit l'un sur l'autre", 2, Construction_batiment)


# Bruitage
Bruitage_mouvement_unite = Tache("Bruitage au déplacement de l'unité", 1, Mouvement_unite)
Bruitage_attaque_unite = Tache("Bruitage lorsque une unité lance une attaque", 1, Attaque_unite)
Bruitage_degat_unite = Tache("Bruitage lorsqu'une unité reçoit des dégat", 1, Attaque_unite)
Bruitage_ordre_unite = Tache("Bruitage lorsque l'unité reçoit un ordre", 1, Mouvement_unite, Attaque_deplacement, Garde_unite)
Bruitage_mort = Tache("Bruitage à la mort d'une unité", 1, Mort_unite)
Bruitage_destruction_batiment = Tache("Bruitage à la destruction du batiment", 1, Destruction_batiment)
Bruitage_interface = Tache("Bruitage des différents boutons des interfaces", 1, Menu_jeu)
Bruitage = Tache("Terminer tout les bruitages du jeu", 1, Bruitage_mouvement_unite, Bruitage_attaque_unite, Bruitage_degat_unite, Bruitage_ordre_unite,
                 Bruitage_mort, Bruitage_destruction_batiment, Bruitage_interface)


# Terrain.
Zone_de_combat = Tache("Créer une zone de combat", 1, Unreal)
Bloquer_unite_zone_combat = Tache("Empecher une unité de sortir de la zone de combat", 3, Zone_de_combat, Mouvement_unite)

# IA.
IA_basique = Tache("Création de la première IA basique desactivable qui envoie des unités attaquer-deplacer le batiment principal du joueur", 3, Destruction_batiment, Batiment_creation_unite, Attaque_unite, Mouvement_unite, Mort_unite)
IA_argent_population = Tache("Modifier l'IA pour qu'elle construise des batiments et prenne en compte l'argent et la population", 3, Ajout_argent, Ajout_population, IA_basique)
IA_avance = Tache("Inventer des stratégies pour l'IA plus efficace et plus intéréssante à jouer contre mais restant au niveau debutant", 8, IA_argent_population)

# Connexion.
Connexion_dans_interface = Tache("Faire connecter des machines dans l'interface de connexion", 6, Interface_connexion)
Tchat_interface_connexion = Tache("Pouvoir envoyer des messages dans le tchat de l'interface de connexion", 2, Connexion_dans_interface)

# Jeu.
Victoire_defaite = Tache("Création d'une victoire et d'une défaite pour les joueurs durant la partie", 2, Destruction_batiment, Empecher_chevauchement_batiment)
Jeu_IA = Tache("Pouvoir jouer contre l'IA", 2, IA_avance, Victoire_defaite)
Jeu_reseau = Tache("Jeu principal en réseau 2 joueurs", 10, Connexion_dans_interface, Attaque_unite, Mort_unite, Destruction_batiment, Batiment_creation_unite, Victoire_defaite)
Raccourci_clavier = Tache("Créer les raccourcies clavier pour l'execution des actions", 2, Creation_batiment_action, Attaque_deplacement, Garde_unite, Mouvement_unite)
Equilibrage = Tache("Equilibrer les différentes variables des créations d'unités", 8, Victoire_defaite, Collision_unite, Selection_multiple, Bloquer_unite_zone_combat)
Equipe_predetermine = Tache("Création d'une équipe prédeterminé", 3, Generation_unite, Generation_batiment, Icones_unite, Modeliser_autre_unite, Equilibrage, Interface_creation_equipe)

# Apres jeu.
Statistique_partie = Tache("Récupérer les statistiques des parties pour analyse", 3, Equilibrage, )
Interface_statistique = Tache("Afficher différentes statistiques sur la partie", 3, Statistique_partie)
Calcul_niveau_joueur = Tache("Chercher à calculer le niveau des joueurs pour améliorer le matchmaking", 2, Victoire_defaite, Jeu_reseau)
Matchmaking = Tache("Générer des matches automatiquement", 3, Victoire_defaite, Jeu_reseau, Raccourci_clavier)
Retour_joueur = Tache("Pouvoir obtenir le retour des joueurs apres une partie", 2, Victoire_defaite)

# Deployement.
Plateforme = Tache("Observer si le jeu fonctionne sur les différentes plateforme concernées", 5, Jeu_IA, Matchmaking, Retour_joueur, Calcul_niveau_joueur, Bruitage, Statistique_partie, Interface_statistique, Equipe_predetermine, Tchat_interface_connexion)
Photo = Tache("Prendre des photos pour la promotion du jeu", 1, Victoire_defaite)
Site_web = Tache("Créer un site web pouvant héberger le jeu", 10, Plateforme)
Forum = Tache("Créer un forum de discution sur le site internet", 4, Site_web)
Publicite = Tache("Envoyer des publicités pour inviter les joueurs à tester le jeu", 6, Forum, Photo)




Gphe = Graphe(*taches)





if __name__ == "__main__":

    print(Gphe.affichage_tableau())
    print("-"*10)
    print("Volume du projet : ")
    print(Gphe.volume())
    print("-"*10)

    fichier = open("data.dot", "w")
    fichier.write(Gphe.dot())
    fichier.close()

    msg = os.popen("dot -Tpng data.dot -o graphe.png")# + " -vv")
    print(msg.read())
    

##    print("Chemin critique : ")
##    for t in Gphe.chemin_critique:
##        print(t,)
