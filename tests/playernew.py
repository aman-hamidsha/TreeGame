import pygame
import random

class Stickman:
    def __init__(self, color, x, y, controls):
        self.color = color
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.can_jump = True
        self.in_air = False
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
        if not self.in_air:
            self.ySpeed = -5
            self.can_jump = True
            self.in_air = False  # Set in_air to True when jumping


RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pygame.init()

size = (800, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Jump")

done = False

clock = pygame.time.Clock()

pygame.mouse.set_visible(1)
red_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP}
blue_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w}

red_stickman = Stickman(RED, 11, 463,red_controls)
blue_stickman = Stickman(BLUE, 700, 200,blue_controls)

stickmen = [red_stickman, blue_stickman]


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        for stickman in stickmen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and stickman.color == RED:
                    stickman.xSpeed = -3
                elif event.key == pygame.K_RIGHT and stickman.color == RED:
                    stickman.xSpeed = 3
                elif event.key == pygame.K_UP and stickman.color == RED and stickman.can_jump:
                    stickman.jump()

                elif event.key == pygame.K_a and stickman.color == BLUE:
                    stickman.xSpeed = -3
                elif event.key == pygame.K_d and stickman.color == BLUE:
                    stickman.xSpeed = 3
                elif event.key == pygame.K_w and stickman.color == BLUE and stickman.can_jump:
                    stickman.jump()

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and stickman.color == RED:
                    stickman.xSpeed = 0

                elif (event.key == pygame.K_a or event.key == pygame.K_d) and stickman.color == BLUE:
                    stickman.xSpeed = 0

    screen.fill(WHITE)

    pygame.draw.line(screen, (0, 0, 0), [size[0] // 2, 0], [size[0] // 2, size[1]], 5)

    

    for stickman in stickmen:
        stickman.ySpeed += 0.2
        stickman.y += stickman.ySpeed
        stickman.x += stickman.xSpeed

        stickman.x = max(0, min(stickman.x, size[0] - 10))
        stickman.y = max(0, min(stickman.y, size[1] - 27))

        # Check for climbing the middle vertical stick
        if (size[0] // 2 - 5 <= stickman.x <= size[0] // 2 + 5) and (stickman.y + 27 >= 0) and (stickman.y <= size[1]):
            stickman.can_jump = True
            stickman.in_air = False  # Reset in_air when landing

        # for platform in platforms:
        #     if (platform.left <= stickman.x <= platform.right) and (platform.top <= stickman.y + 27 <= platform.bottom) and stickman.ySpeed > 0:
        #         stickman.y = platform.top - 27
        #         stickman.ySpeed = 0
        #         stickman.can_jump = True

    for stickman in stickmen:
        stickman.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
