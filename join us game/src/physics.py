def calculate_angle(circle_x, circle_y, mouse_x, mouse_y):
    import math
    return math.atan2(mouse_y - circle_y, mouse_x - circle_x)

def apply_force(circle, mouse_x, mouse_y, force):
    angle = calculate_angle(circle.x, circle.y, mouse_x, mouse_y)
    circle.speed_x += force * math.cos(angle)
    circle.speed_y += force * math.sin(angle)