import pygame as pg
from pygame.math import Vector2
import random
import pretty_errors
from src import branch, branchGenerator, player, leaf

screen = Vector2(1000, 600)
inMenu = True

# initialize pygame and create window
pg.init()
pg.mixer.init()




screen = pg.display.set_mode((screen.x, screen.y))
pg.display.set_caption("Tree climber")
clock = pg.time.Clock() # needed for constant fps
FPS = 60

branch.Branch.midpoint = int(screen.get_width()/2)
leaf.Leaf.image = pg.image.load("imgs/leaf.png").convert()

map = branchGenerator.BranchGenerator(screen.get_height()-1000, 35, screen.get_height())


p1 = player.Player(0, 0)
l1 = leaf.Leaf(Vector2(screen.get_width()//2, screen.get_height()//2), 90)






# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pg.font.Font(None, 36)
play_text = font.render("Play", True, white)

# Texts
title_text = font.render("Tree Race", True, black)
title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

play_text = font.render("Play", True, white)
play_rect = play_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))


# Game loop
running = True
while running:
    clock.tick(FPS)

        # allows you to quit the game if you hit the x button in the top-right
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    # keeps the game running at constant fps
    if not inMenu:
        # background screen colour
        screen.fill(pg.Color("aqua"))

        keys = pg.key.get_pressed()
        p1.Update(keys, screen)

        # drawing the randomly-generated tree
        pg.draw.rect(screen, pg.Color("brown"), pg.Rect(screen.get_width()/2-25, 0, 50, screen.get_height()))
        map.Update(screen, screen.get_height(), 0, p1)

        screen.blit(p1.image, p1.rect)

        
    else:
        if event.type == pg.MOUSEBUTTONDOWN:
            inMenu = False
    
    # update changes to screen
    pg.display.update()

pg.quit()
