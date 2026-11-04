# -*- coding: utf-8 -*-
import pygame
import sys
import math
import numpy as np
from quiz_bank import SCIENCE_SECTIONS
from game_assets import draw_lion_asset, draw_deer_asset, draw_plant_asset, draw_stone_asset, draw_human_asset, draw_confetti
from entities import KidButton, RewardStars, FoodSprite

try:
    import android
    android.init()
except ImportError:
    pass

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

COLOR_BG = (44, 62, 80) 
COLOR_PANEL = (52, 73, 94)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (230, 126, 34)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Science Journey Pro Stable")
clock = pygame.time.Clock()

def play_educational_sound(sound_type):
    duration = 0.2
    sample_rate = 22050
    n_samples = int(duration * sample_rate)
    
    if sound_type == "CORRECT":
        frequencies = [523.25, 659.25, 783.99, 1046.50]
        samples = np.array([], dtype=np.int16)
        for freq in frequencies:
            t = np.linspace(0, duration/4, int(n_samples/4), False)
            sig = np.sin(2 * np.pi * freq * t) * 16383
            samples = np.append(samples, sig.astype(np.int16))
    elif sound_type == "EXPLAIN":
        t = np.linspace(0, duration, n_samples, False)
        samples = (np.sin(2 * np.pi * 330 * t) * 12000).astype(np.int16)
    else:
        t = np.linspace(0, 0.1, int(sample_rate * 0.1), False)
        samples = (np.sin(2 * np.pi * 587 * t) * 10000).astype(np.int16)
        
    sound = pygame.mixer.Sound(buffer=samples)
    sound.play()

class AppManager:
    def __init__(self):
        self.state = "MENU" 
        self.previous_state = "MENU"
        self.selected_section = "LIVING"
        self.q_idx = 0
        self.score = 0
        self.show_celebration = False
        self.celebration_timer = 0
        self.stars = []
        
        self.btn_start = KidButton(SCREEN_WIDTH//2 - 280, 440, 240, 80, (46, 204, 113), (39, 174, 96))
        self.btn_go_minigame = KidButton(SCREEN_WIDTH//2 + 40, 440, 240, 80, (155, 89, 182), (142, 68, 173))
        
        self.sec_buttons = {
            "LIVING": KidButton(60, 320, 260, 110, (155, 89, 182), (142, 68, 173)),
            "PLANTS": KidButton(360, 320, 260, 110, (39, 174, 96), (30, 130, 76)),
            "ANIMALS": KidButton(660, 320, 260, 110, (230, 126, 34), (211, 84, 0)),
            "HUMAN": KidButton(960, 320, 260, 110, (231, 76, 60), (192, 57, 43))
        }
        
        self.btn_exit_yes = KidButton(SCREEN_WIDTH//2 - 220, 400, 180, 70, (192, 57, 43), (150, 40, 30))
        self.btn_exit_no = KidButton(SCREEN_WIDTH//2 + 40, 400, 180, 70, (46, 204, 113), (30, 150, 80))

        self.lion_target_rect = pygame.Rect(250, 200, 200, 200)
        self.deer_target_rect = pygame.Rect(800, 200, 200, 200)
        self.foods = [
            FoodSprite(450, 500, "MEAT"),
            FoodSprite(700, 500, "GRASS")
        ]

    def setup_quiz_options(self):
        questions = SCIENCE_SECTIONS[self.selected_section]
        if self.q_idx < len(questions):
            q_data = questions[self.q_idx]
            self.opt_buttons = []
            for i, opt in enumerate(q_data["opts"]):
                ox = SCREEN_WIDTH//2 - 400 + (i * 280)
                self.opt_buttons.append((KidButton(ox, 520, 250, 75, (52, 152, 219), (41, 128, 185)), opt))

manager = AppManager()

def draw_hud():
    pygame.draw.rect(screen, COLOR_PANEL, (0, 0, SCREEN_WIDTH, 60))
    pygame.draw.rect(screen, (241, 196, 15), (20, 15, min(300, manager.score * 10), 30), border_radius=10)

def main_loop():
    running = True
    while running:
        screen.fill(COLOR_BG)
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_AC_BACK:
                    if manager.state != "CONFIRM_EXIT":
                        manager.previous_state = manager.state
                        manager.state = "CONFIRM_EXIT"
                        play_educational_sound("CLICK")
                    else:
                        manager.state = manager.previous_state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    click = True
                    if manager.state == "MINI_GAME":
                        for food in manager.foods:
                            if food.rect.collidepoint((mx, my)):
                                food.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and manager.state == "MINI_GAME":
                    for food in manager.foods:
                        if food.dragging:
                            food.dragging = False
                            if food.food_type == "MEAT" and manager.lion_target_rect.collidepoint((mx, my)):
                                manager.score += 20
                                manager.show_celebration = True
                                manager.celebration_timer = 30
                                play_educational_sound("CORRECT")
                            elif food.food_type == "GRASS" and manager.deer_target_rect.collidepoint((mx, my)):
                                manager.score += 20
                                manager.show_celebration = True
                                manager.celebration_timer = 30
                                play_educational_sound("CORRECT")
                            food.reset_position()

        if manager.state == "MINI_GAME":
            for food in manager.foods:
                if food.dragging:
                    food.rect.x = mx - 45
                    food.rect.y = my - 45

        if manager.state == "MENU":
            draw_plant_asset(screen, SCREEN_WIDTH//2 - 250, 220, 50)
            draw_human_asset(screen, SCREEN_WIDTH//2 + 250, 220, 45)
            draw_lion_asset(screen, SCREEN_WIDTH//2, 220, 55)
            
            manager.btn_start.draw(screen)
            manager.btn_go_minigame.draw(screen)
            
            pygame.draw.polygon(screen, COLOR_TEXT, [(SCREEN_WIDTH//2 - 170, 440), (SCREEN_WIDTH//2 - 170, 500), (SCREEN_WIDTH//2 - 135, 480)])
            pygame.draw.circle(screen, COLOR_TEXT, (SCREEN_WIDTH//2 + 160, 480), 12)
            
            if click:
                if manager.btn_start.rect.collidepoint((mx, my)):
                    manager.state = "SECTION_SELECT"
                    play_educational_sound("CLICK")
                elif manager.btn_go_minigame.rect.collidepoint((mx, my)):
                    manager.state = "MINI_GAME"
                    manager.score = 0
                    play_educational_sound("EXPLAIN")

        elif manager.state == "MINI_GAME":
            draw_hud()
            pygame.draw.rect(screen, COLOR_PANEL, (100, 100, SCREEN_WIDTH - 200, 540), border_radius=25)
            pygame.draw.rect(screen, (52, 73, 94), manager.lion_target_rect, border_radius=20)
            pygame.draw.rect(screen, (52, 73, 94), manager.deer_target_rect, border_radius=20)
            
            draw_lion_asset(screen, manager.lion_target_rect.centerx, manager.lion_target_rect.centery, 55)
            draw_deer_asset(screen, manager.deer_target_rect.centerx, manager.deer_target_rect.centery, 50)
            
            for food in manager.foods:
                food.draw(screen)
                
            if manager.show_celebration:
                draw_confetti(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                manager.celebration_timer -= 1
                if manager.celebration_timer <= 0: manager.show_celebration = False

        elif manager.state == "SECTION_SELECT":
            for sec_key, btn in manager.sec_buttons.items():
                btn.draw(screen)
                if sec_key == "LIVING": draw_stone_asset(screen, btn.rect.centerx, btn.rect.centery - 80, 30)
                elif sec_key == "PLANTS": draw_plant_asset(screen, btn.rect.centerx, btn.rect.centery - 80, 35)
                elif sec_key == "ANIMALS": draw_lion_asset(screen, btn.rect.centerx, btn.rect.centery - 80, 40)
                elif sec_key == "HUMAN": draw_human_asset(screen, btn.rect.centerx, btn.rect.centery - 80, 35)
                
                if click and btn.rect.collidepoint((mx, my)):
                    manager.selected_section = sec_key
                    manager.q_idx = 0
                    manager.score = 0
                    manager.setup_quiz_options()
                    manager.state = "PLAYING"
                    play_educational_sound("EXPLAIN")

        elif manager.state == "PLAYING":
            draw_hud()
            questions = SCIENCE_SECTIONS[manager.selected_section]
            
            if manager.q_idx < len(questions):
                q_data = questions[manager.q_idx]
                pygame.draw.rect(screen, COLOR_PANEL, (120, 90, SCREEN_WIDTH - 240, 400), border_radius=25)
                
                if manager.selected_section == "LIVING": draw_stone_asset(screen, SCREEN_WIDTH//2, 340, 40)
                elif manager.selected_section == "PLANTS": draw_plant_asset(screen, SCREEN_WIDTH//2, 340, 40)
                elif manager.selected_section == "ANIMALS": draw_lion_asset(screen, SCREEN_WIDTH//2, 340, 45)
                elif manager.selected_section == "HUMAN": draw_human_asset(screen, SCREEN_WIDTH//2, 340, 40)

                for btn, opt_text in manager.opt_buttons:
                    btn.draw(screen)
                    pygame.draw.circle(screen, COLOR_TEXT, (btn.rect.x + 30, btn.rect.y + 38), 10)
                    
                    if click and btn.rect.collidepoint((mx, my)):
                        if opt_text == q_data["ans"]:
يُرجى استخدام الرمز البرمجي بحذر.
manager.score += 10
manager.show_celebration = True
manager.celebration_timer = 30
manager.stars.append(RewardStars(btn.rect.centerx, btn.rect.centery))
play_educational_sound("CORRECT")
else:
play_educational_sound("CLICK")
manager.q_idx += 1
manager.setup_quiz_options()
if manager.q_idx < len(questions):
play_educational_sound("EXPLAIN")
break
else:
manager.state = "SECTION_SELECT"
if manager.show_celebration:
draw_confetti(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
manager.celebration_timer -= 1
if manager.celebration_timer <= 0: manager.show_celebration = False
for star in manager.stars:
star.draw(screen)
if len(manager.stars) > 5: manager.stars.pop(0)
elif manager.state == "CONFIRM_EXIT":
pygame.draw.rect(screen, COLOR_PANEL, (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 200, 600, 350), border_radius=30)
pygame.draw.rect(screen, COLOR_ACCENT, (SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 200, 600, 350), 4, border_radius=30)
pygame.draw.polygon(screen, (241, 196, 15), [(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 140), (SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 - 80), (SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT//2 - 80)])
manager.btn_exit_yes.draw(screen)
manager.btn_exit_no.draw(screen)
if click:
if manager.btn_exit_yes.rect.collidepoint((mx, my)):
running = False
if manager.btn_exit_no.rect.collidepoint((mx, my)):
manager.state = manager.previous_state
play_educational_sound("CLICK")
pygame.display.flip()
clock.tick(60)
pygame.quit()
sys.exit()
if name == "main":
main_loop()
