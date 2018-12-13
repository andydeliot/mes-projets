import pygame
from pygame import *
import pygame.gfxdraw
from random import randint, choice
from copy import copy

pygame.init()
SURFACE = 900

main_surface = pygame.display.set_mode((SURFACE, SURFACE))

# Set up some data to describe a small rectangle and its color
small_rect = (300, 200, 150, 90)
some_color = (255, 0, 0)        # A color is a mix of (Red, Green, Blue)


taux_ajout = 10
taux_suppression = 10
taux_changement = 10

class Line:
    def __init__(self):
        self.x1 = randint(0, SURFACE)
        self.y1 = randint(0, SURFACE)
        self.x2 = randint(0, SURFACE)
        self.y2 = randint(0, SURFACE)
        self.color = (255, 255, 255)

    def update(self):
        valeur = randint(1, 100)
        if valeur <= taux_changement:
            self.x1 = randint(0, SURFACE)
        valeur = randint(1, 100)
        if valeur <= taux_changement:
            self.y1 = randint(0, SURFACE)
        valeur = randint(1, 100)
        if valeur <= taux_changement:
            self.x2 = randint(0, SURFACE)
        valeur = randint(1, 100)
        if valeur <= taux_changement:
            self.y2 = randint(0, SURFACE)




lines = [Line() for _ in range(1)]
lines_saved = list(lines)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                break
            if event.key == K_p: # Content.
                lines_saved = [copy(line) for line in lines]
            if event.key == K_o: # Pas content.
                lines = [copy(line) for line in lines_saved]

            # Modification des lines.
            for line in lines:
                line.update()
                
            while True:
                valeur = randint(1, 100)
                if valeur <= taux_ajout:
                    lines.append(Line())
                else:
                    break
            while True:
                valeur = randint(1, 100)
                if valeur <= taux_suppression and len(lines)>1:
                    lines.remove(choice(lines))
                else:
                    break


    # Background.
    main_surface.fill((0, 200, 255))

    for line in lines:
        pygame.gfxdraw.line(main_surface, line.x1, line.y1, line.x2, line.y2,
                            line.color)



    pygame.display.flip()










pygame.quit()     # Once we leave the loop, close the window.







































