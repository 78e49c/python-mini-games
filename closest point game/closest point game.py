import pygame
import random
import math

# Window size
WIDTH, HEIGHT = 750, 500
PANEL_HEIGHT = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bright = False

    def draw(self, screen):
        color = WHITE if self.bright else GRAY
        pygame.draw.circle(screen, color, (self.x, self.y), 2)

# Generate a new random coordinate
def get_new_random_point():
    return random.randint(0, WIDTH), random.randint(PANEL_HEIGHT, HEIGHT)

# Restart the game
def reset_game():
    global points, random_x, random_y, game_won
    points = []
    random_x, random_y = get_new_random_point()
    game_won = False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("closest point game")
font = pygame.font.SysFont(None, 30)

# Initial points
points = []
random_x, random_y = get_new_random_point()
game_won = False

def find_closest_point():
    closest_point = None
    min_distance = float('inf')
    
    for point in points:
        distance = math.hypot(point.x - random_x, point.y - random_y)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
            
        # Check if the player has won
        if distance <= 25:
            global game_won
            game_won = True
    
    return closest_point

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_won:
                x, y = event.pos
                if y > PANEL_HEIGHT:  # Ensure the top panel is not clicked
                    new_point = Point(x, y)
                    points.append(new_point)

                    closest_point = find_closest_point()
                    if closest_point:
                        for point in points:
                            point.bright = False
                        closest_point.bright = True
            
    # Update screen
    screen.fill(BLACK)
    
    # Draw points
    for point in points:
        point.draw(screen)

    # Draw top panel
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, PANEL_HEIGHT))
    
    # Show point count
    point_count_text = font.render(f'Point Count: {len(points)}', True, WHITE)
    screen.blit(point_count_text, (10, 10))
    
    # Display win message
    if game_won:
        win_text = font.render('Congratulations, You Found It!', True, WHITE)
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)
    
    # Draw reset button
    reset_button = pygame.Rect(WIDTH - 165, 5, 160, 30)
    pygame.draw.rect(screen, BLACK, reset_button)
    reset_button_text = font.render('Restart', True, WHITE)
    screen.blit(reset_button_text, (WIDTH - 80, 10))
    
    pygame.display.flip()

    # Handle mouse clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if reset_button.collidepoint(mouse_pos) and mouse_pressed[0]:
        reset_game()

pygame.quit()
