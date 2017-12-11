# coding=utf-8

import cProfile
import ctypes

import pygame
from pygame import *
from time import time

try:
    from Pygamebuilder.Vision import Vision
except:
    from Vision import Vision

def creation_ecran():
    """ Permet de créer des écrans adapté à chaque ordinateur. """
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        ecran = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
    except AttributeError:
        ecran = pygame.display.set_mode((1800, 1000))
    return ecran


class Game:
    pygame.init()

    Ecran = creation_ecran()
    LARGEUR_ECRAN, HAUTEUR_ECRAN = Ecran.get_width(), Ecran.get_height()
    CENTREX = LARGEUR_ECRAN / 2
    CENTREY = HAUTEUR_ECRAN / 2

    # Ecran.
    PIXEL_PAR_METRE = 12  # Nombres de pixels pour 1 metre.
    LARGEUR_ECRAN_METRE, HAUTEUR_ECRAN_METRE = LARGEUR_ECRAN / PIXEL_PAR_METRE, HAUTEUR_ECRAN / PIXEL_PAR_METRE
    COULEUR_FOND_ECRAN = (0, 0, 0)

    # Vitesse de jeu.
    HERTZ = 125  # Nombres d'images par secondes.
    PERIODE = 1. / HERTZ
    Clock = pygame.time.Clock()

    # Objet.
    Vision = Vision()
    objets = []  # Liste de tout les objets qui seront updaté dans last_update.
    textes = []  # Textes écrans.
    boutons = []  # Boutons écrans.
    personnages = []
    projectiles = []

    # Controle.
    continuer = True
    touche_appuyes = ()
    events = []
    pygame.key.set_repeat(10, 10)
    etat_clic_gauche = False
    etat_clic_droit = False

    # Info.
    Profileur = cProfile.Profile()
    profiliation = False
    temps_de_boucle = time()
    paufination = False

    def __init__(self):
        pass

    # Gestion du jeu.

    @staticmethod
    def reinitialiser_jeu():
        Game.objets = []
        Game.personnages = []
        Game.projectiles = []

    @staticmethod
    def reinitialiser_tout():

        # Ecran.
        Game.LARGEUR_ECRAN, Game.HAUTEUR_ECRAN = Game.Ecran.get_width(), Game.Ecran.get_height()
        Game.CENTREX = Game.LARGEUR_ECRAN / 2
        Game.CENTREY = Game.HAUTEUR_ECRAN / 2

        # Ecran.
        Game.PIXEL_PAR_METRE = 12  # Nombres de pixels pour 1 metre.
        Game.LARGEUR_ECRAN_METRE, Game.HAUTEUR_ECRAN_METRE = Game.LARGEUR_ECRAN / Game.PIXEL_PAR_METRE, Game.HAUTEUR_ECRAN / Game.PIXEL_PAR_METRE
        Game.COULEUR_FOND_ECRAN = (0, 0, 0)

        # Vitesse de jeu.
        Game.HERTZ = 125  # Nombres d'images par secondes.
        Game.PERIODE = 1. / Game.HERTZ
        Game.Clock = pygame.time.Clock()

        # Objet.
        Game.Vision = Vision()
        Game.objets = []  # Liste de tout les objets qui seront updaté dans last_update.
        Game.textes = []  # Textes écrans.
        Game.boutons = []  # Boutons écrans.
        Game.personnages = []
        Game.projectiles = []

        # Controle.
        Game.continuer = True
        Game.touche_appuyes = ()
        Game.events = []
        pygame.key.set_repeat(10, 10)
        Game.etat_clic_gauche = False
        Game.etat_clic_droit = False

        # Info.
        Game.Profileur = cProfile.Profile()
        Game.profiliation = False
        Game.temps_de_boucle = time()
        Game.paufination = False

        # Reinitialisation de pygame.
        pygame.mouse.set_visible(True)

    @staticmethod
    def jouer():
        if Game.continuer:
            Game.last_update()
            if Game.paufination:
                Game.calcul_fps()
            Game.first_update()
            Game.controle()
            return True
        Game.quit()
        return False

    @staticmethod
    def quit():
        if Game.profiliation:
            Game.Profileur.disable()
            Game.Profileur.create_stats()
            Game.Profileur.print_stats()

        pygame.quit()

    @staticmethod
    def definir_ips(ips):
        Game.HERTZ = ips
        Game.PERIODE = 1. / Game.HERTZ

    # Information performance.
    @staticmethod
    def profiler():
        Game.profiliation = True
        Game.Profileur.enable()

    @staticmethod
    def paufiner():
        Game.paufination = True
    @staticmethod
    def calcul_fps():
        nouveau_temps_de_boucle = time() - Game.temps_de_boucle
        try:
            fps = 1. / nouveau_temps_de_boucle
        except ZeroDivisionError:
            fps = "Infini"
        print(fps)
        # tempsVoulu = 1 / Game.HERTZ
        # if nouveau_temps_de_boucle < tempsVoulu:
        #     pygame.time.delay(int((tempsVoulu - nouveau_temps_de_boucle) * 1000))
        Game.temps_de_boucle = time()

    # Information ecran.
    @staticmethod
    def get_centre():
        return Game.CENTREX, Game.CENTREY

    # Update.
    @staticmethod
    def first_update():
        Game.Clock.tick(Game.HERTZ)
        Game.Ecran.fill(Game.COULEUR_FOND_ECRAN)
        Game.touche_appuyes = pygame.key.get_pressed()
        Game.events = list(pygame.event.get())
        Game.controle()

    @staticmethod
    def last_update():
        for bouton in Game.boutons:
            bouton.update()

        for texte in Game.textes:
            texte.update()

        Game.objets = sorted(Game.objets, key=lambda x: x.priorite_affichage)
        for objet in list(Game.objets):
            objet.update()

        pygame.display.flip()

    # Control utilisateur.
    @staticmethod
    def controle():
        for event in Game.events:
            # Le joueur appuye sur Echap.
            if event.type == KEYUP and event.key == K_ESCAPE: Game.continuer = False
            # Controler l'état de la souris.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: Game.etat_clic_gauche = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: Game.etat_clic_droit = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: Game.etat_clic_gauche = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3: Game.etat_clic_droit = False

    @staticmethod
    def bouton_appuye(pygame_key):
        return Game.touche_appuyes[pygame_key]

    @staticmethod
    def clic_gauche():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False

    @staticmethod
    def declic_gauche():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                return True
        return False

    @staticmethod
    def clic_droit():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                return True
        return False

    @staticmethod
    def declic_droit():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                return True
        return False

    @staticmethod
    def clic_molette():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                return True
        return False

    @staticmethod
    def declic_molette():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                return True
        return False

    @staticmethod
    def molette_haut():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                return True
        return False

    @staticmethod
    def molette_bas():
        for event in Game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                return True
        return False

    @staticmethod
    def mouvement_souris():
        for event in Game.events:
            if event.type == pygame.MOUSEMOTION:
                return True
        return False

    @staticmethod
    def position_souris():
        return pygame.mouse.get_pos()


class MetaGame(type):
    """ Ceci est la classe qu'il faut hériter en méta type:
    class MonJeu(metaclass=Pygamebuilder.MetaGame):
        MonJeu.couleur_fond_ecran=(255, 255, 255)
    """

    def __new__(mcs, name, bases, dct):
        for cle, value in dct.items():
            setattr(Game, cle, value)
        return super().__new__(mcs, name, bases, dct)

    def __getattribute__(self, item):
        return type.__getattribute__(Game, item)

    def __setattr__(self, name, value):
        setattr(Game, name, value)


if __name__ == "__main__":
    while Game.jouer():
        Game.controle()





    
