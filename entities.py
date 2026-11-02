import pygame
import math

class KidButton:
    def __init__(self, x, y, w, h, color, accent_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.accent_color = accent_color

    def draw(self, surface, is_active=False):
        c = self.accent_color if is_active else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=20)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=20)

class RewardStars:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pulse = 0

    def draw(self, surface):
        self.pulse += 0.2
        r = int(20 + math.sin(self.pulse) * 5)
        points = []
        for i in range(5):
            angle = i * 4 * math.pi / 5
            pt_x = self.x + int(r * math.cos(angle))
            pt_y = self.y + int(r * math.sin(angle))
            points.append((pt_x, pt_y))
        if len(points) == 5:
            pygame.draw.polygon(surface, (241, 196, 15), points)

class FoodSprite:
    def __init__(self, start_x, start_y, food_type):
        self.rect = pygame.Rect(start_x, start_y, 90, 90)
        self.base_x = start_x
        self.base_y = start_y
        self.food_type = food_type
        self.dragging = False

    def draw(self, surface):
        if self.food_type == "MEAT":
            pygame.draw.ellipse(surface, (192, 57, 43), self.rect)
            pygame.draw.circle(surface, (236, 240, 241), (self.rect.x + 10, self.rect.centery), 12)
            pygame.draw.circle(surface, (236, 240, 241), (self.rect.x + 20, self.rect.centery), 8)
        else:
            pygame.draw.ellipse(surface, (39, 174, 96), self.rect)
            pygame.draw.ellipse(surface, (46, 204, 113), (self.rect.x + 15, self.rect.y + 10, 60, 40))

    def reset_position(self):
        self.rect.x = self.base_x
        self.rect.y = self.base_y
        self.dragging = False
