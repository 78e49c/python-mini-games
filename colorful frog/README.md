# Colorful Frog

Colorful Frog is a game where you control a central ball and shoot projectiles to hit moving balls. The goal is to hit as many balls as possible while managing your ball lives.

## How to Play

1. **Starting the Game**: The game starts with 10 ball lives. The central ball is displayed in the middle of the screen with the current ball lives shown in the center.

2. **Shooting Projectiles**: Click anywhere on the screen to shoot a projectile from the central ball towards the clicked position. Each shot decreases your ball lives by 1.

3. **Hitting Balls**: 
   - If a projectile hits a moving ball, the ball is destroyed, and you gain ball lives based on the distance of the hit:
     - 0-99 distance: 1 ball life
     - 100-199 distance: 2 ball lives
     - 200-299 distance: 3 ball lives
     - 300-399 distance: 4 ball lives
     - 400-499 distance: 5 ball lives
     - 500-599 distance: 6 ball lives
     - 600-699 distance: 7 ball lives
     - 700+ distance: 8 ball lives
   - If the color of the hit ball matches the current color of the central ball, the gained ball lives are doubled.

4. **Avoiding the Center**: If a moving ball gets too close to the center (within 30 units), you lose 10 ball lives.

5. **Game Over**: If your ball lives drop below 0, the game ends. A "Game Over" screen is displayed with your final score. Click anywhere on the screen to restart the game.

6. **Score Display**: The top right corner of the screen displays your current score, which is the total number of balls hit.

## Controls

- **Mouse Click**: Shoot a projectile towards the clicked position.
- **Mouse Click (Game Over)**: Restart the game.

## Installation

1. Ensure you have Python and Pygame installed.
2. Clone this repository.
3. Run the `colorful_frog.py` file.

```bash
git clone https://github.com/yourusername/colorful-frog.git
cd colorful-frog
python colorful_frog.py
