import pygame
import random

def draw_lion_asset(surface, x, y, size):
    pygame.draw.circle(surface, (230, 126, 34), (x, y), int(size * 0.7)) 
    pygame.draw.circle(surface, (241, 196, 15), (x, y), int(size * 0.5)) 
    pygame.draw.circle(surface, (44, 62, 80), (x - int(size*0.15), y - int(size*0.1)), 6)
    pygame.draw.circle(surface, (44, 62, 80), (x + int(size*0.15), y - int(size*0.1)), 6)
    pygame.draw.polygon(surface, (192, 57, 43), [(x, y), (x - 8, y + 10), (x + 8, y + 10)])

def draw_deer_asset(surface, x, y, size):
    pygame.draw.circle(surface, (211, 84, 0), (x, y), int(size * 0.5))
    pygame.draw.ellipse(surface, (211, 84, 0), (x - int(size*0.4), y - int(size*0.4), 20, 40))
    pygame.draw.ellipse(surface, (211, 84, 0), (x + int(size*0.2), y - int(size*0.4), 20, 40))
    pygame.draw.circle(surface, (0, 0, 0), (x - 10, y - 5), 5)
    pygame.draw.circle(surface, (0, 0, 0), (x + 10, y - 5), 5)
    pygame.draw.circle(surface, (44, 62, 80), (x, y + 10), 6)

def draw_plant_asset(surface, x, y, size):
    pygame.draw.lines(surface, (139, 69, 19), False, [(x, y + 40), (x - 15, y + 60), (x + 15, y + 75)], 3)
    pygame.draw.rect(surface, (39, 174, 96), (x - 6, y - 20, 12, 60), border_radius=3)
    pygame.draw.ellipse(surface, (46, 204, 113), (x + 6, y, 25, 15))
    pygame.draw.ellipse(surface, (46, 204, 113), (x - 31, y - 10, 25, 15))
    pygame.draw.circle(surface, (231, 76, 60), (x, y - 30), 20)
    pygame.draw.circle(surface, (241, 196, 15), (x, y - 30), 8)

def draw_stone_asset(surface, x, y, size):
    pygame.draw.polygon(surface, (127, 140, 141), [(x-30, y+20), (x-10, y-20), (x+30, y-10), (x+40, y+20), (x, y+35)])
    pygame.draw.polygon(surface, (149, 165, 166), [(x-10, y-20), (x+30, y-10), (x, y+35)])

def draw_human_asset(surface, x, y, size):
    pygame.draw.circle(surface, (253, 227, 167), (x, y - 10), int(size * 0.5))
    pygame.draw.circle(surface, (255, 255, 255), (x - 12, y - 15), 10)
    pygame.draw.circle(surface, (255, 255, 255), (x + 12, y - 15), 10)
    pygame.draw.circle(surface, (41, 128, 185), (x - 12, y - 15), 5)
    pygame.draw.circle(surface, (41, 128, 185), (x + 12, y - 15), 5)
    pygame.draw.arc(surface, (231, 76, 60), (x - 15, y - 10, 30, 20), 3.14, 0, 3)
    pygame.draw.circle(surface, (231, 76, 60), (x, y + 35), 12)

def draw_confetti(surface, screen_width, screen_height):
    for _ in range(15):
        cx = random.randint(100, screen_width - 100)
        cy = random.randint(50, 300)
        rc = random.choice([(26, 188, 156), (46, 204, 113), (155, 89, 182), (241, 196, 15), (231, 76, 60)])
        pygame.draw.circle(surface, rc, (cx, cy), random.randint(5, 12))
