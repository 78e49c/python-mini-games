import pygame
import math
import random
from circle import Circle

pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 750
FPS = 60
FRICTION = 0.98
VELOCITY_INCREMENT_INTERVAL = 100  # milliseconds
VELOCITY = 3
ENEMY_VELOCITY = 5
ENEMY_SPAWN_INTERVAL = 1000  # milliseconds

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("join us game")

# Create an instance of the Circle class
circle = Circle(WIDTH // 2, HEIGHT // 2, radius=8, color=(255, 255, 255))

# Font for the timer
font = pygame.font.Font(None, 36)

# Main game loop
clock = pygame.time.Clock()
running = True
last_velocity_increment_time = 0
last_enemy_spawn_time = 0
start_time = pygame.time.get_ticks()
enemies = []

def spawn_enemy():
    x = random.choice([0, WIDTH])
    y = random.choice([0, HEIGHT])
    return Circle(x, y, radius=8, color=(255, 0, 0))

def reset_game():
    global circle, enemies, start_time, last_velocity_increment_time, last_enemy_spawn_time, running
    circle = Circle(WIDTH // 2, HEIGHT // 2, radius=8, color=(255, 255, 255))
    enemies = []
    start_time = pygame.time.get_ticks()
    last_velocity_increment_time = 0
    last_enemy_spawn_time = 0
    running = True

reset_game()

while True:
    current_time = pygame.time.get_ticks()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not running and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            reset_game()

    if running:
        if mouse_pressed[0] and current_time - last_velocity_increment_time > VELOCITY_INCREMENT_INTERVAL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - circle.y, mouse_x - circle.x)
            circle.vx += VELOCITY * math.cos(angle)
            circle.vy += VELOCITY * math.sin(angle)
            last_velocity_increment_time = current_time

        if mouse_pressed[2] and current_time - last_velocity_increment_time > VELOCITY_INCREMENT_INTERVAL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - circle.y, mouse_x - circle.x)
            circle.vx -= VELOCITY * math.cos(angle)
            circle.vy -= VELOCITY * math.sin(angle)
            last_velocity_increment_time = current_time

        if current_time - last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
            enemies.append(spawn_enemy())
            last_enemy_spawn_time = current_time

        # Update circle position
        circle.update()

        # Ensure the circle stays within the window bounds
        circle.x = max(circle.radius, min(circle.x, WIDTH - circle.radius))
        circle.y = max(circle.radius, min(circle.y, HEIGHT - circle.radius))

        # Update enemies position
        for enemy in enemies:
            angle = math.atan2(circle.y - enemy.y, circle.x - enemy.x)
            enemy.vx = ENEMY_VELOCITY * math.cos(angle)
            enemy.vy = ENEMY_VELOCITY * math.sin(angle)
            enemy.update()

        # Check for collisions between enemies
        new_enemies = []
        merged = set()
        for i, enemy1 in enumerate(enemies):
            if i in merged:
                continue
            for j, enemy2 in enumerate(enemies):
                if i != j and j not in merged and math.hypot(enemy1.x - enemy2.x, enemy1.y - enemy2.y) < enemy1.radius + enemy2.radius:
                    new_enemies.append(Circle.merge(enemy1, enemy2))
                    merged.add(i)
                    merged.add(j)
                    break
            else:
                new_enemies.append(enemy1)
        enemies = new_enemies

        # Check for collision with the player's circle
        for enemy in enemies:
            if math.hypot(circle.x - enemy.x, circle.y - enemy.y) < circle.radius + enemy.radius:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the circle
        circle.draw(screen)

        # Draw the enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw the timer
        elapsed_time = (current_time - start_time) // 1000
        timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
    else:
        # Display the survival time
        screen.fill((0, 0, 0))
        game_over_text = font.render(f"Game Over! You survived for {elapsed_time} seconds.", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()