import pygame as pg
from pygame import Vector2

class Player():
    def __init__(self, x, y):
        self.image = pg.Surface((10, 30))
        # self.image.fill(pg.Color("red"))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = Vector2(0, 0)
        self.gravity = 1
        self.terminalVelocity = 10
        self.prevRect = self.rect.copy()
        RED = (255, 0, 0)
        self.draw(self.image,RED)
        self.canJump = True 

    def Update(self, keys: list, screen: pg.Surface):
        self.RegisterInput(keys)
        self.MovePlayer(screen)

    def MovePlayer(self, screen):

        # saves the location of the player before they move
        # effectively shows what the player was like last frame
        self.prevRect = self.rect.copy()

        if self.velocity.y < self.terminalVelocity:
            self.velocity.y += self.gravity
        
        self.rect.y += self.velocity.y
        self.rect.x += self.velocity.x

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.canJump = True

    def RegisterInput(self, keys: list):
        if keys[pg.K_UP] and self.canJump:
            self.velocity.y = -15
            self.canJump = False

        
        if keys[pg.K_LEFT]:
            self.velocity.x = -5
        elif keys[pg.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0

    def draw(self, player, color):
        # head
        pg.draw.ellipse(player, color, [0, 0, 10, 10], 0)
        # body
        pg.draw.line(player, color, [4, 17], [4, 7], 2)
        # legs
        pg.draw.line(player, color, [4, 17], [9, 27], 2)
        pg.draw.line(player, color, [4, 17], [-1, 27], 2)
        # arms
        pg.draw.line(player, color, [4, 7], [8, 17], 2)
        pg.draw.line(player, color, [4, 7], [0, 17], 2)

        player.set_colorkey((0,0,0))


