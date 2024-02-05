import pygame
import random

class Stickman:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.can_jump = False

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

red_stickman = Stickman(RED, 11, 463)
blue_stickman = Stickman(BLUE, 700, 200)

stickmen = [red_stickman, blue_stickman]

# Adding 5 more platforms to bottom left and bottom right
bottom_left_platforms = [pygame.Rect(0, 490, 50, 10), pygame.Rect(50, 470, 50, 10),
                          pygame.Rect(100, 450, 50, 10), pygame.Rect(150, 430, 50, 10),
                          pygame.Rect(200, 410, 50, 10)]

bottom_right_platforms = [pygame.Rect(size[0] - 50, 490, 50, 10), pygame.Rect(size[0] - 100, 470, 50, 10),
                           pygame.Rect(size[0] - 150, 450, 50, 10), pygame.Rect(size[0] - 200, 430, 50, 10),
                           pygame.Rect(size[0] - 250, 410, 50, 10)]

# Adding 10 more platforms in random places
random_platforms = [pygame.Rect(random.randint(250, 550), random.randint(150, 350), 73, 10) for _ in range(10)]

# Adding all platforms attached to the center vertical line
center_vertical_line = size[0] // 2
for platform in bottom_left_platforms + bottom_right_platforms + random_platforms:
    platform.left = center_vertical_line - (platform.width // 2)

platforms = [
    pygame.Rect(100, 490, 200, 10),
    pygame.Rect(400, 390, 200, 10),
    pygame.Rect(0, 290, 200, 10),
    pygame.Rect(500, 200, 200, 10),
    pygame.Rect(200, 100, 200, 10),
    pygame.Rect(600, 50, 200, 10),
    pygame.Rect(500, 290, 200, 10),
    pygame.Rect(50, 200, 73, 10),
    pygame.Rect(150, 150, 73, 10),
    pygame.Rect(250, 100, 73, 10),
    pygame.Rect(350, 50, 73, 10),
    pygame.Rect(550, 150, 73, 10),
    pygame.Rect(650, 100, 73, 10),
    pygame.Rect(750, 50, 73, 10),
    pygame.Rect(0, 400, 200, 10),
    pygame.Rect(100, 350, 200, 10),
    pygame.Rect(200, 300, 200, 10),
    pygame.Rect(300, 250, 200, 10),
    pygame.Rect(400, 200, 200, 10),
    pygame.Rect(500, 150, 200, 10),
    pygame.Rect(600, 100, 200, 10),
    pygame.Rect(700, 50, 200, 10),
]

platforms.extend(bottom_left_platforms + bottom_right_platforms + random_platforms)

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

    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 0), platform)

    for stickman in stickmen:
        stickman.ySpeed += 0.2
        stickman.y += stickman.ySpeed
        stickman.x += stickman.xSpeed

        stickman.x = max(0, min(stickman.x, size[0] - 10))
        stickman.y = max(0, min(stickman.y, size[1] - 27))

        # Check for climbing the middle vertical stick
        if (size[0] // 2 - 5 <= stickman.x <= size[0] // 2 + 5) and (stickman.y + 27 >= 0) and (stickman.y <= size[1]):
            stickman.can_jump = True

        for platform in platforms:
            if (platform.left <= stickman.x <= platform.right) and (platform.top <= stickman.y + 27 <= platform.bottom) and stickman.ySpeed > 0:
                stickman.y = platform.top - 27
                stickman.ySpeed = 0
                stickman.can_jump = True

    for stickman in stickmen:
        stickman.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
