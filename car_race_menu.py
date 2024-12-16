import pygame
import sys
import subprocess  # For running external scripts

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
try:
    background = pygame.image.load("assets/image/poster.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error:
    print("Background image not found. Using a solid color background.")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))  # Black background fallback

# Load sounds
try:
    pygame.mixer.music.load("assets/sound/026491_pixel-song-8-72675.mp3")  # Background music
    pygame.mixer.music.play(-1)  # Loop indefinitely
    button_click_sound = pygame.mixer.Sound("assets/sound/Button_click_sound_sound_effect.mp3")
except pygame.error as e:
    print(f"Error loading sound: {e}")

# Fonts
font = pygame.font.Font(None, 36)

# Button Positions
play_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
quit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 470, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_button(rect, text, default_color, hover_color):
    """Draw a button with hover effect."""
    color = hover_color if rect.collidepoint(pygame.mouse.get_pos()) else default_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def main_menu():
    """Main menu loop."""
    while True:
        screen.blit(background, (0, 0))  # Draw background image

        # Draw buttons with hover effects
        draw_button(play_button_rect, "Play", DARK_GREEN, (0, 255, 0))
        draw_button(quit_button_rect, "Quit", DARK_RED, (255, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    # Stop the background music
                    pygame.mixer.music.stop()

                    # Play button sound and start game
                    button_click_sound.play()
                    pygame.time.delay(500)  # Wait for sound to finish
                    try:
                        subprocess.run([sys.executable, "car_race.py"])
                    except Exception as e:
                        print(f"Error launching game: {e}")
                elif quit_button_rect.collidepoint(event.pos):
                    # Play button sound and quit
                    button_click_sound.play()
                    pygame.time.delay(500)  # Wait for sound to finish
                    pygame.quit()
                    sys.exit()

        # Refresh display
        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
    main_menu()
