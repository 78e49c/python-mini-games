import pygame
import math

class Circle:
    def __init__(self, x, y, radius=8, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.color = color
        self.friction = 0.98

    def update(self):
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Apply friction
        self.vx *= self.friction
        self.vy *= self.friction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def area(self):
        return math.pi * (self.radius ** 2)

    @staticmethod
    def merge(circle1, circle2):
        new_x = (circle1.x + circle2.x) / 2
        new_y = (circle1.y + circle2.y) / 2
        new_area = circle1.area() + circle2.area()
        new_radius = math.sqrt(new_area / math.pi)
        return Circle(new_x, new_y, new_radius)