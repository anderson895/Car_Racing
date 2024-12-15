import pygame
import random
import sys
import subprocess  # Import subprocess to navigate to the main menu

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Race Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (50, 180, 50)  # Grass green
GRAY = (100, 100, 100)  # Road color
YELLOW = (255, 255, 0)  # Road lane markings

# Car Dimensions
CAR_WIDTH = 50
CAR_HEIGHT = 100

# Road Dimensions
ROAD_WIDTH = 500
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2

# Global variables for scores
highest_score = 0  # Tracks the highest score

# Load images
try:
    PLAYER_CAR_IMAGE = pygame.image.load("assets/blue_car-removebg-preview.png")
    ENEMY_CAR_IMAGE = pygame.image.load("assets/red_car_-removebg-preview.png")

    # Scale images to match car dimensions
    PLAYER_CAR_IMAGE = pygame.transform.scale(PLAYER_CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
    ENEMY_CAR_IMAGE = pygame.transform.scale(ENEMY_CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))
except pygame.error:
    print("Error: Unable to load car images. Please ensure the image files exist.")
    pygame.quit()
    exit()


# Button Class
class Button:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.current_color = button_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.button_color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False


# Player Car Class
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_CAR_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_X:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < (ROAD_X + ROAD_WIDTH):
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


# Enemy Car Class
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, occupied_lanes):
        super().__init__()
        self.image = ENEMY_CAR_IMAGE
        self.rect = self.image.get_rect()

        # Lanes: Divide the road into 5 lanes
        lanes = [0, 1, 2, 3, 4]
        available_lanes = [lane for lane in lanes if lane not in occupied_lanes]

        # If all lanes are occupied, clear the oldest entry to ensure space
        if not available_lanes:
            occupied_lanes.pop(0)  # Remove the oldest lane
            available_lanes = [lane for lane in lanes if lane not in occupied_lanes]

        # Randomly choose one of the available lanes
        self.lane = random.choice(available_lanes)
        occupied_lanes.append(self.lane)  # Mark this lane as occupied

        # Position the car in the chosen lane
        lane_width = ROAD_WIDTH // 5
        self.rect.x = ROAD_X + self.lane * lane_width + (lane_width - self.rect.width) // 2
        self.rect.y = random.randint(-300, -100)  # Spawn above the screen

        # Set speed for the car
        self.speed = random.uniform(3, 6)

    def update(self):
        # Move the car downward
        self.rect.y += self.speed

        # Reset position if car goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.y = random.randint(-300, -100)


# Drawing the road and grass
def draw_road_and_grass(lane_y_offset):
    SCREEN.fill(GREEN)
    pygame.draw.rect(SCREEN, GRAY, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    lane_width = ROAD_WIDTH // 5
    lane_spacing = 100

    # Draw lane markings
    for lane in range(1, 5):  # Draw 4 lane separators
        x = ROAD_X + lane * lane_width
        for y in range(-lane_spacing, SCREEN_HEIGHT, lane_spacing):
            adjusted_y = y + lane_y_offset
            pygame.draw.rect(SCREEN, YELLOW, (x - 5, adjusted_y, 10, 50))


# Pause Screen
def pause_game():
    font = pygame.font.Font(None, 64)
    small_font = pygame.font.Font(None, 36)
    resume_button = Button(
        SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 140, 50,
        "Resume", small_font, WHITE, GREEN, (0, 200, 0)
    )
    menu_button = Button(
        SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 50, 140, 50,
        "Main Menu", small_font, WHITE, BLUE, (0, 0, 200)
    )
    quit_button = Button(
        SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 20, 140, 50,
        "Quit", small_font, WHITE, RED, (200, 0, 0)
    )

    while True:
        SCREEN.fill(GRAY)
        pause_text = font.render("Paused", True, WHITE)
        SCREEN.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)))

        resume_button.draw(SCREEN)
        menu_button.draw(SCREEN)
        quit_button.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if resume_button.handle_event(event):
                return
            if menu_button.handle_event(event):
                subprocess.run([sys.executable, "car_race_menu.py"])
                pygame.quit()
                sys.exit()
            if quit_button.handle_event(event):
                pygame.quit()
                exit()

        pygame.display.flip()


# Game Over Screen
def game_over_screen(screen, score):
    global highest_score

    # Update the highest score
    if score > highest_score:
        highest_score = score

    # Fonts
    title_font = pygame.font.Font(None, 64)
    button_font = pygame.font.Font(None, 36)

    # Buttons
    continue_button = Button(
        SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 140, 50,
        "Continue", button_font, WHITE, GREEN, (0, 200, 0)
    )
    quit_button = Button(
        SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 50, 140, 50,
        "Quit", button_font, WHITE, RED, (200, 0, 0)
    )

    running = True
    while running:
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        game_over_text = title_font.render("Game Over", True, WHITE)
        score_text = button_font.render(f"Score: {score}", True, WHITE)
        high_score_text = button_font.render(f"Highest Score: {highest_score}", True, WHITE)
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
        screen.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))

        continue_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if continue_button.handle_event(event):
                return True
            if quit_button.handle_event(event):
                return False

        pygame.display.flip()
    return False


# Main Game Loop
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    while True:
        all_sprites = pygame.sprite.Group()
        enemy_cars = pygame.sprite.Group()

        player = PlayerCar()
        all_sprites.add(player)

        score = 0
        difficulty_timer = 0
        max_enemy_cars = 3
        lane_y_offset = 0
        lane_speed = 2
        running = True

        # List to track occupied lanes
        occupied_lanes = []

        pause_button = Button(
            SCREEN_WIDTH - 60, 10, 50, 40,
            "||", font, WHITE, GRAY, (150, 150, 150)
        )

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if pause_button.handle_event(event):
                    pause_game()

            # Increase difficulty
            difficulty_timer += 1
            if difficulty_timer % 500 == 0 and max_enemy_cars < 10:
                max_enemy_cars += 1
                lane_speed += 1

            # Add new enemy cars if needed
            if len(enemy_cars) < max_enemy_cars:
                enemy = EnemyCar(occupied_lanes)
                enemy_cars.add(enemy)
                all_sprites.add(enemy)

            # Update all sprites
            all_sprites.update()

            # Detect collisions
            if pygame.sprite.spritecollideany(player, enemy_cars):
                if not game_over_screen(SCREEN, score):
                    return
                break

            # Draw everything
            lane_y_offset = (lane_y_offset + lane_speed) % 100
            draw_road_and_grass(lane_y_offset)

            pause_button.draw(SCREEN)
            all_sprites.draw(SCREEN)

            # Update score
            score += 1
            score_text = font.render(f"Score: {score}", True, WHITE)
            SCREEN.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
