import pygame
class Stickman:
    def __init__(self, color, x, y, controls):
        self.color = color
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.can_jump = False
        self.controls = controls  # Dictionary to store controls

    def draw(self, screen):
        # head
        pygame.draw.ellipse(screen, self.color, [0+self.x, 0+self.y, 10, 10], 0)
        # body
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [4+self.x, 7+self.y], 2)
        # legs
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [9+self.x, 27+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [-1+self.x, 27+self.y], 2)
        # arms
        pygame.draw.line(screen, self.color, [4+self.x, 7+self.y], [8+self.x, 17+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 7+self.y], [0+self.x, 17+self.y], 2)

    def jump(self):
        if self.can_jump:
            self.ySpeed = -5
            self.can_jump = False
