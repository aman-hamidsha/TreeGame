import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 1  # Adjust this value to control the strength of gravity

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (123,42,0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)

    def update(self):
        self.velocity.y += GRAVITY  # Apply gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity.x = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = 0


class Branch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((300, 5))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity in Pygame")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player(WIDTH // 2, HEIGHT // 2)
branch1 = Branch(WIDTH // 2, HEIGHT // 2)
branch2 = Branch(WIDTH // 200, HEIGHT // 5)
all_sprites.add(player, branch1, branch2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.velocity.y = -5
    elif keys[pygame.K_DOWN]:
        player.velocity.y = 5
    else:
        player.velocity.x = 0

    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
