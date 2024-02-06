import pygame as pg
from pygame import Vector2
import random

class Leaf:
    def __init__(self, pivot, rotation):
        scaler = random.randint(1, 3)
        self.image = pg.transform.scale(self.image, (scaler*self.image.get_width(), scaler*self.image.get_height()))
        self.l = self.image.get_width()
        self.w = self.image.get_height()
        self.rotation = rotation
        self.pivot = pivot
        self.RotateOnPivot()

    def RotateOnPivot(self):
        self.image = pg.transform.rotate(self.image, -self.rotation)
        centerDisplacement = Vector2(self.l/2-self.w/2, 0)
        
        self.newPosCenter = self.pivot + centerDisplacement.rotate(self.rotation)
        self.rect = self.image.get_rect(center = self.newPosCenter)
        self.image.set_colorkey((0,0,0))
    
    def Draw(self, screen):
        screen.blit(self.image, self.rect)