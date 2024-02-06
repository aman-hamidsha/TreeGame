import pygame as pg
from pygame.math import Vector2
import random
import pretty_errors
from src import branch, branchGenerator, player

screen = Vector2(1000, 600)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((screen.x, screen.y))
pg.display.set_caption("Tree cliber")
clock = pg.time.Clock() # needed for constant fps
FPS = 60

# needed to tell branches at what x-position to spawn
branch.Branch.midpoint = int(screen.get_width()/2)

map = branchGenerator.BranchGenerator(screen.get_height()-1000, 40, screen.get_height())

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

    # AMAN ---------------------------------------------------------------------------------_#
    # p1 is the player, replace that with whatever your player object is
    # i'll add support for the second player later
    # for optimisation, I'm not checking if the left player is colliding with the right branches because that should never happen in the first place anyway
    map.Update(screen, screen.get_height(), 0, p1)

    # update changes to screen
    pg.display.update()

pg.quit()