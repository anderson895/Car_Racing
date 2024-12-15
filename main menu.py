import pygame
import sys
import subprocess  # Import subprocess to run external scripts

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 600

# Colors
DARK_GREEN = (0, 180, 0)  # Darker Green
DARK_RED = (200, 0, 0)    # Darker Red
WHITE = (255, 255, 255)

# Button Properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race Menu")

# Load background image
background = pygame.image.load("assets/poster.png")  # Ensure your image is saved here
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)

# Button Positions
play_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
quit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 470, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.blit(background, (0, 0))  # Draw background image

        # Draw buttons (now darker colors)
        draw_button(play_button_rect, "Play", DARK_GREEN)
        draw_button(quit_button_rect, "Quit", DARK_RED)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    print("Play Button Pressed!")
                    # Launch car_race.py
                    subprocess.run([sys.executable, "car_race.py"])
                elif quit_button_rect.collidepoint(event.pos):
                    print("Quit Button Pressed!")
                    pygame.quit()
                    sys.exit()

        # Refresh display
        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
    main_menu()