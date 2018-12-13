

from combat import *

import pygame
from pygame import gfxdraw
from pygame import *

from random import randint, choice

pygame.init()
pygame.font.init()

Ecran = pygame.display.set_mode((800, 800))
myfont = pygame.font.SysFont('Comic Sans MS', 40)

T = Terrain(10, 10, Ecran)
P1 = Personnage((0, 0, 100), 9, 9)
P2 = Personnage((100, 0, 0), 4, 8)
T.ajouter_personnage(P1, P2)
T.personnage_suivant()

S1 = Sort(P1,
          conditions=[pa, pa, pa, pm, portee, portee, portee, zone, zone],
          applications=[degat, ralentissement, ralentissement, ralentissement])
S2 = Sort(P2,
          conditions=[pa, pa, pa, pm, pm, portee, portee, portee, portee, portee_minimum],
          applications=[degat, degat, fatigue, fatigue])
S3 = Sort(P1,
          conditions=[],
          applications=[vitesse])
S4 = Sort(P2,
          conditions=[],
          applications=[energie])

S5 = Sort(P1,
          conditions=[portee, portee, portee, portee, pa, pa],
          applications=[ajouter_etat(poison(conditions=[duree, duree]))])

S6 = Sort(P2,
          conditions=[pa, pa, pa, pa, pa, zone, zone],
          applications=[ajouter_etat(bouclier(conditions=[duree]))])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                T.personnage_actif.deplacement_haut()
            elif event.key == K_DOWN:
                T.personnage_actif.deplacement_bas()
            elif event.key == K_LEFT:
                T.personnage_actif.deplacement_gauche()
            elif event.key == K_RIGHT:
                T.personnage_actif.deplacement_droite()
            elif event.key == K_RETURN:
                T.personnage_suivant()

            elif event.key == K_a:
                T.personnage_actif.sort = T.personnage_actif.sorts[0]
            elif event.key == K_z:
                T.personnage_actif.sort = T.personnage_actif.sorts[1]
            elif event.key == K_e:
                T.personnage_actif.sort = T.personnage_actif.sorts[2]


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if T.personnage_actif.sort is not None:
                    case_cible = T.clic_case(event.pos)
                    T.personnage_actif.sort.run(case_cible, T)
        if event.type == pygame.MOUSEMOTION:
            try:
                if T.personnage_actif.sort.check_conditions(T.clic_case(event.pos), T):
                    T.case_selectionnees = T.zonage(T.clic_case(event.pos),
                                                    T.personnage_actif.sort.zone,
                                                    T.personnage_actif.sort.zone_minimum)
                else:
                    T.case_selectionnees = []
            except AttributeError:
                pass
    T.run()
    
    Ecran.fill((0,0,0))
    T.update(Ecran)
    
    textsurface = myfont.render(str(T.personnage_actif), True, (255, 255, 255))
    Ecran.blit(textsurface,(0,0))
    
    pygame.display.update()


























        

    


















        
