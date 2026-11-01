"""Reusable UI entities and touch handling."""
import math
import random
import pygame


class Button:
    def __init__(self, rect, label, color=(255, 184, 77), value=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.value = value if value is not None else label

    def draw(self, surface, text_fn, hover=False):
        color = tuple(min(255, c+18) for c in self.color) if hover else self.color
        pygame.draw.rect(surface, (80, 87, 125), self.rect.move(0, 6), border_radius=20)
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=20)
        text_fn(surface, self.label, self.rect.center, max(20, self.rect.height//3), (55, 57, 78))

    def contains(self, pos):
        return self.rect.collidepoint(pos)


class FloatingStar:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.life = 1.0
        self.vy = random.uniform(-120, -65)
        self.size = random.randint(12, 24)

    def update(self, dt):
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return
        points = []
        for i in range(10):
            a = -math.pi/2 + i*math.pi/5
            r = self.size if i % 2 == 0 else self.size*0.45
            points.append((self.x+math.cos(a)*r, self.y+math.sin(a)*r))
        pygame.draw.polygon(surface, (255, 218, 65), points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)


class Confetti:
    COLORS = [(255, 93, 121), (75, 205, 170), (255, 207, 72), (115, 155, 255)]

    def __init__(self, x, y, count=30):
        self.particles = []
        for _ in range(count):
            self.particles.append([
                x, y, random.uniform(-150, 150), random.uniform(-210, -60),
                random.uniform(0.8, 1.8), random.choice(self.COLORS),
            ])

    def update(self, dt):
        for p in self.particles:
            p[0] += p[2]*dt
            p[1] += p[3]*dt
            p[3] += 220*dt
            p[4] -= dt

    def draw(self, surface):
        for x, y, _, _, life, color in self.particles:
            if life > 0:
                pygame.draw.rect(surface, color, (int(x), int(y), 7, 10), border_radius=2)


class ProgressBar:
    def __init__(self, rect, total):
        self.rect = pygame.Rect(rect)
        self.total = max(1, total)
        self.value = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=12)
        fill = self.rect.copy()
        fill.width = int(self.rect.width * min(1, self.value/self.total))
        if fill.width:
            pygame.draw.rect(surface, (69, 196, 137), fill, border_radius=12)


class TouchTracker:
    """Tracks mouse and finger events using the same logical coordinates."""
    def __init__(self):
        self.down_pos = None
        self.last_pos = None

    def events(self, event, size):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.down_pos = event.pos
            self.last_pos = event.pos
            return "down", event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            self.down_pos = None
            self.last_pos = pos
            return "up", pos
        if event.type == pygame.FINGERDOWN:
            pos = (int(event.x*size[0]), int(event.y*size[1]))
            self.down_pos = pos
            self.last_pos = pos
            return "down", pos
        if event.type == pygame.FINGERUP:
            pos = (int(event.x*size[0]), int(event.y*size[1]))
            self.down_pos = None
            self.last_pos = pos
            return "up", pos
        if event.type == pygame.FINGERMOTION:
            pos = (int(event.x*size[0]), int(event.y*size[1]))
            self.last_pos = pos
            return "move", pos
        return None, None
