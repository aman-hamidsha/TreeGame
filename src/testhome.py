import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tree Race")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Texts
title_text = font.render("Tree Race", True, black)
title_rect = title_text.get_rect(center=(width // 2, height // 4))

play_text = font.render("Play", True, white)
play_rect = play_text.get_rect(center=(width // 2, height // 2))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                print("Play button clicked!")  # You can replace this with your actual game code

    # Draw background
    screen.fill(white)

    # Draw title
    screen.blit(title_text, title_rect)

    # Draw play button
    pygame.draw.rect(screen, black, play_rect)
    screen.blit(play_text, play_rect)

    # Update display
    pygame.display.flip()
