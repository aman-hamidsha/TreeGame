import pygame as pg
from pygame import Vector2

class Player():
    def __init__(self, x, y):
        self.image = pg.Surface((50, 50))
        self.image.fill(pg.Color("red"))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = Vector2(0, 0)
        self.gravity = 2
        self.terminalVelocity = 10
        self.prevRect = self.rect.copy()

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

    def RegisterInput(self, keys: list):
        if keys[pg.K_UP]:
            self.velocity.y = -30
        
        if keys[pg.K_LEFT]:
            self.velocity.x = -5
        elif keys[pg.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0



class Stickman:
    def __init__(self, color, x, y,controls):
        self.color = color
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.can_jump = True
        self.in_air = False
        self.controls = controls # 0 for arrows 1 for WASD
        # self.rect = self.get_rect()
        # self.rect.center = (x, y)
        # self.prevRect = self.rect.copy()
        

    def draw(self, screen):
        # head
        pg.draw.ellipse(screen, self.color, [0+self.x, 0+self.y, 10, 10], 0)
        # body
        pg.draw.line(screen, self.color, [4+self.x, 17+self.y], [4+self.x, 7+self.y], 2)
        # legs
        pg.draw.line(screen, self.color, [4+self.x, 17+self.y], [9+self.x, 27+self.y], 2)
        pg.draw.line(screen, self.color, [4+self.x, 17+self.y], [-1+self.x, 27+self.y], 2)
        # arms
        pg.draw.line(screen, self.color, [4+self.x, 7+self.y], [8+self.x, 17+self.y], 2)
        pg.draw.line(screen, self.color, [4+self.x, 7+self.y], [0+self.x, 17+self.y], 2)

    def jump(self):
        if not self.in_air:
            self.ySpeed = -5
            self.can_jump = True
            self.in_air = False  # Set in_air to True when jumping

    def RegisterInput(self, keys: list):
        if self.controls == 0:
            if keys[pg.K_UP]:
                self.jump()
            elif keys[pg.K_LEFT]:
                self.xSpeed = -3
            elif keys[pg.K_RIGHT]:
                self.xSpeed = 3
        else:
            if keys[pg.K_w]:
                self.jump()
            elif keys[pg.K_a]:
                self.xSpeed = -3
            elif keys[pg.K_d]:
                self.xSpeed = 3

    def MovePlayer(self, screen):
        # saves the location of the player before they move
        # effectively shows what the player was like last frame
        # self.prevRect = self.rect.copy()

        self.ySpeed += 2
        
        self.y += self.ySpeed
        self.x += self.xSpeed

        if self.left < 0:
            self.left = 0
            self.xSpeed = 0
        elif self.right > screen.get_width():
            self.right = screen.get_width()

        if self.top < 0:
            self.top = 0
            self.ySpeed = 0
        elif self.bottom > screen.get_height():
            self.bottom = screen.get_height()

    def Update(self, keys: list, screen: pg.Surface):
        self.RegisterInput(keys)
        self.MovePlayer(screen)
