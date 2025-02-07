import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Orbital Motion")

# Colors
black = (32, 32, 32)
red = (255, 0, 0)
white = (255, 255, 255)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Ball properties
red_ball_radius = 20
red_ball_pos = (width // 2, height // 2)
angle = 0
radius = 400
speed = 0.05

# Projectile properties
projectiles = []
projectile_speed = 15

# Orbital balls
orbital_balls = []
spawn_distance = 700  # Distance from the center where new balls will spawn
orbital_ball_speed = 0.5  # Speed of the orbital balls
orbital_ball_radius = 15

# Game properties
ball_lives = 10
current_color = red
font = pygame.font.SysFont(None, 55)
score_font = pygame.font.SysFont(None, 35)
top_hits = 0

# Fragment properties
fragment_count = 5
fragment_speed = 15
fragments = []
fragment_lifetime = 15  # Lifetime of fragments in frames

def calculate_angle(center, point):
    return math.atan2(center[1] - point[1], center[0] - point[0])

def reset_game():
    global ball_lives, current_color, projectiles, orbital_balls, fragments, top_hits
    ball_lives = 10
    current_color = red
    projectiles = []
    orbital_balls = []
    fragments = []
    top_hits = 0

# Main loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            red_ball_pos = (width // 2, height // 2)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
                game_over = False
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - red_ball_pos[1], mouse_x - red_ball_pos[0])
                projectiles.append([red_ball_pos[0], red_ball_pos[1], angle])
                ball_lives -= 1  # Decrease ball lives when a projectile is fired

    if not game_over:
        # Update projectiles
        for projectile in projectiles[:]:
            projectile[0] += math.cos(projectile[2]) * projectile_speed
            projectile[1] += math.sin(projectile[2]) * projectile_speed

            # Remove projectile if it goes off screen
            if projectile[0] < 0 or projectile[0] > width or projectile[1] < 0 or projectile[1] > height:
                projectiles.remove(projectile)

        # Update fragments
        for fragment in fragments[:]:
            fragment[0] += math.cos(fragment[2]) * fragment_speed
            fragment[1] += math.sin(fragment[2]) * fragment_speed
            fragment[4] -= 1  # Decrease lifetime

            # Remove fragment if it goes off screen or lifetime is over
            if fragment[0] < 0 or fragment[0] > width or fragment[1] < 0 or fragment[1] > height or fragment[4] <= 0:
                fragments.remove(fragment)

        # Check for collisions
        for projectile in projectiles[:]:
            hit = False
            for ball in orbital_balls[:]:
                if math.hypot(projectile[0] - ball[0], projectile[1] - ball[1]) < red_ball_radius:
                    distance = math.hypot(ball[0] - red_ball_pos[0], ball[1] - red_ball_pos[1])
                    orbital_balls.remove(ball)
                    projectiles.remove(projectile)
                    points = max(1, distance // 100)
                    if ball[2] == current_color:
                        ball_lives += 2 * points
                    else:
                        ball_lives += points
                    current_color = random.choice(colors)  # Change the color after a hit
                    hit = True
                    top_hits += 1

                    # Create fragments
                    center_angle = calculate_angle(red_ball_pos, ball)
                    opposite_angle = (center_angle + math.pi) % (2 * math.pi)
                    for _ in range(fragment_count):
                        fragment_angle = random.uniform(opposite_angle - math.pi / 6, opposite_angle + math.pi / 6)
                        fragments.append([ball[0], ball[1], fragment_angle, ball[2], fragment_lifetime])

                    break

        # Check if any ball is too close to the center
        for ball in orbital_balls[:]:
            if math.hypot(ball[0] - red_ball_pos[0], ball[1] - red_ball_pos[1]) < 30:
                ball_lives -= 10
                orbital_balls.remove(ball)

        # Check if ball lives are negative
        if ball_lives < 0:
            game_over = True

        # Spawn new orbital balls
        if pygame.time.get_ticks() % 1000 < 50:
            angle = random.uniform(0, 2 * math.pi)
            spawn_x = red_ball_pos[0] + int(spawn_distance * math.cos(angle))
            spawn_y = red_ball_pos[1] + int(spawn_distance * math.sin(angle))
            color = random.choice(colors)
            orbital_balls.append([spawn_x, spawn_y, color, spawn_distance, angle])

        # Update orbital balls
        for ball in orbital_balls[:]:
            ball[4] += orbital_ball_speed * speed
            ball[0] = red_ball_pos[0] + int(ball[3] * math.cos(ball[4]))
            ball[1] = red_ball_pos[1] + int(ball[3] * math.sin(ball[4]))
            ball[3] -= 1  # Decrease the distance to the center to simulate approaching

            # Remove ball if it goes off screen
            if ball[3] < 0:
                orbital_balls.remove(ball)

    # Draw everything
    screen.fill(black)

    # Draw concentric circles
    max_radius = max(width, height)
    for r in range(100, max_radius, 100):
        pygame.draw.circle(screen, white, red_ball_pos, r, 1)

    for projectile in projectiles:
        pygame.draw.circle(screen, white, (int(projectile[0]), int(projectile[1])), 5)
    for ball in orbital_balls:
        pygame.draw.circle(screen, ball[2], (int(ball[0]), int(ball[1])), orbital_ball_radius)
    for fragment in fragments:
        pygame.draw.circle(screen, fragment[3], (int(fragment[0]), int(fragment[1])), orbital_ball_radius // 2)

    # Draw remaining ball lives
    if not game_over:
        lives_text = font.render(str(int(ball_lives)), True, current_color)
        text_rect = lives_text.get_rect(center=(red_ball_pos[0], red_ball_pos[1]))
        screen.blit(lives_text, text_rect)

    # Draw top hits
    score_text = score_font.render(f"Score: {top_hits}", True, white)
    screen.blit(score_text, (width - 150, 10))

    if game_over:
        game_over_text = font.render("Game Over", True, red)
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        final_score_text = font.render(f"Final Score: {top_hits}", True, red)
        final_score_rect = final_score_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(final_score_text, final_score_rect)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()