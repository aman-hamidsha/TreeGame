import pygame
import random

class Player:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.can_jump = False

    def move(self, direction):
        if direction == "left":
            self.xSpeed = -3
        elif direction == "right":
            self.xSpeed = 3

    def stop(self):
        self.xSpeed = 0

    def jump(self):
        if self.can_jump:
            self.ySpeed = -5
            self.can_jump = False

    def update(self):
        self.ySpeed += 0.2
        self.y += self.ySpeed
        self.x += self.xSpeed

        self.x = max(0, min(self.x, size[0] - 10))
        self.y = max(0, min(self.y, size[1] - 27))

        # Check for climbing the middle vertical stick
        if (size[0] // 2 - 5 <= self.x <= size[0] // 2 + 5) and (self.y + 27 >= 0) and (self.y <= size[1]):
            self.can_jump = True

        for platform in platforms:
            if (platform.left <= self.x <= platform.right) and (platform.top <= self.y + 27 <= platform.bottom) and self.ySpeed > 0:
                self.y = platform.top - 27
                self.ySpeed = 0
                self.can_jump = True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, [0+self.x, 0+self.y, 10, 10], 0)
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [4+self.x, 7+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [9+self.x, 27+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 17+self.y], [-1+self.x, 27+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 7+self.y], [8+self.x, 17+self.y], 2)
        pygame.draw.line(screen, self.color, [4+self.x, 7+self.y], [0+self.x, 17+self.y], 2)


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

red_player = Player(RED, 11, 463)
blue_player = Player(BLUE, 700, 200)

players = [red_player, blue_player]

# Rest of the code remains the same

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        for player in players:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.color == RED:
                    player.move("left")
                elif event.key == pygame.K_RIGHT and player.color == RED:
                    player.move("right")
                elif event.key == pygame.K_UP and player.color == RED and player.can_jump:
                    player.jump()

                elif event.key == pygame.K_a and player.color == BLUE:
                    player.move("left")
                elif event.key == pygame.K_d and player.color == BLUE:
                    player.move("right")
                elif event.key == pygame.K_w and player.color == BLUE and player.can_jump:
                    player.jump()

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and player.color == RED:
                    player.stop()

                elif (event.key == pygame.K_a or event.key == pygame.K_d) and player.color == BLUE:
                    player.stop()

    screen.fill(WHITE)

    pygame.draw.line(screen, (0, 0, 0), [size[0] // 2, 0], [size[0] // 2, size[1]], 5)

    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 0), platform)

    for player in players:
        player.update()
        player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
