import pygame as pg
from pygame.math import Vector2
import random
import pretty_errors
from src import branch, branchGenerator

screen = Vector2(1000, 600)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((screen.x, screen.y))
pg.display.set_caption("Tree cliber")
clock = pg.time.Clock() # needed for constant fps
FPS = 30

# needed to tell branches at what x-position to spawn
branch.Branch.midpoint = int(screen.get_width()/2)

map = branchGenerator.BranchGenerator(screen.get_height()-1000, 40, screen.get_height())

b = branch.ThickBranch(int(screen.get_height()/2))

# Game loop
running = True
while running:

    # keeps the game running at constant fps
    clock.tick(FPS)

    # allows you to quit the game if you hit the x button in the top-right
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # background screen colour
    screen.fill(pg.Color("aqua"))

    # drawing the randomly-generated tree
    pg.draw.rect(screen, pg.Color("brown"), pg.Rect(screen.get_width()/2-25, 0, 50, screen.get_height()))
    map.Draw(screen, screen.get_height(), 0)

    # update changes to screen
    pg.display.update()

pg.quit()