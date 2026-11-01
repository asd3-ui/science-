"""Mغامرات العلوم: Arabic educational mini-games for children."""
import os
import random
import pygame

from game_assets import draw_animal, draw_background
from quiz_bank import ANIMALS, TRIVIA, RIDDLES, DIETS, DIET_HINTS
from entities import Button, FloatingStar, Confetti, ProgressBar, TouchTracker

WIDTH, HEIGHT = 960, 540
FONT_PATHS = [
    os.environ.get("ARABIC_FONT", ""),
    "assets/NotoNaskhArabic-Regular.ttf",
    "/system/fonts/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


class ScienceGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("مغامرات العلوم")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font_path = next((p for p in FONT_PATHS if p and os.path.isfile(p)), None)
        self.small = self._font(23)
        self.medium = self._font(30)
        self.large = self._font(44)
        self.state = "menu"
        self.previous = ["menu"]
        self.touch = TouchTracker()
        self.stars = []
        self.confetti = []
        self.score = 0
        self.round_index = 0
        self.message = ""
        self.message_timer = 0
        self.leaderboard = []
        self.buttons = []
        self.setup_game()

    def _font(self, size):
        # Explicit font file only: no platform-dependent SysFont(None, ...).
        if self.font_path:
            try:
                return pygame.font.Font(self.font_path, size)
            except pygame.error:
                pass
        return pygame.font.Font(pygame.font.get_default_font(), size)

    def text(self, surface, value, center, size=28, color=(50, 57, 78)):
        font = self._font(size)
        text = str(value)
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            text = get_display(arabic_reshaper.reshape(text))
        except Exception:
            pass
        image = font.render(text, True, color)
        surface.blit(image, image.get_rect(center=(int(center[0]), int(center[1]))))

    def setup_game(self):
        self.buttons = []
        self.round_index = 0
        if self.state == "identify":
            self.identify_order = random.sample(ANIMALS, len(ANIMALS))
            self.progress = ProgressBar((350, 32, 260, 22), len(self.identify_order))
        elif self.state == "feeder":
            self.feeder_order = random.sample(ANIMALS, len(ANIMALS))
            self.progress = ProgressBar((350, 32, 260, 22), len(self.feeder_order))
        elif self.state == "trivia":
            self.trivia_order = random.sample(TRIVIA, len(TRIVIA))
            self.progress = ProgressBar((350, 32, 260, 22), len(self.trivia_order))

    def go(self, state):
        self.previous.append(self.state)
        self.state = state
        self.message = ""
        if state in ("identify", "feeder", "trivia"):
            self.setup_game()

    def back(self):
        if self.state == "menu":
            return
        self.state = self.previous.pop() if self.previous else "menu"
        self.buttons = []

    def add_button(self, rect, label, color, action):
        self.buttons.append((Button(rect, label, color, action), action))

    def draw_panel(self, title):
        draw_background(self.screen, pygame.time.get_ticks()/1000)
        pygame.draw.rect(self.screen, (255, 250, 227), (35, 24, WIDTH-70, HEIGHT-48), border_radius=30)
        pygame.draw.rect(self.screen, (255, 255, 255), (35, 24, WIDTH-70, HEIGHT-48), 4, border_radius=30)
        self.text(self.screen, title, (WIDTH//2, 65), 36, (57, 86, 113))
        self.text(self.screen, f"⭐ {self.score}", (WIDTH-115, 65), 27, (207, 139, 28))

    def menu(self):
        self.draw_panel("مغامرات العلوم")
        self.text(self.screen, "هيا نكتشف عالم الحيوانات والطبيعة!", (WIDTH//2, 130), 25)
        items = [
            ("من أنا؟", "identify", (255, 184, 77)),
            ("أطعم الحيوان", "feeder", (92, 203, 158)),
            ("أسئلة العلماء", "trivia", (111, 165, 245)),
            ("لوحة الأبطال", "leaderboard", (223, 133, 197)),
        ]
        for i, (label, state, color) in enumerate(items):
            x = 145 + i*175
            self.add_button((x, 230, 150, 100), label, color, ("go", state))
        for i, a in enumerate(ANIMALS[:4]):
            draw_animal(self.screen, a["name"], (160+i*210, 420), 0.55, pygame.time.get_ticks()/1000)

    def identify(self):
        animal = self.identify_order[self.round_index]
        self.draw_panel("من أنا؟")
        self.progress.value = self.round_index
        self.progress.draw(self.screen)
        self.text(self.screen, animal["trait"], (WIDTH//2, 130), 26)
        draw_animal(self.screen, animal["name"], (WIDTH//2, 270), 1.0, pygame.time.get_ticks()/1000)
        names = random.sample([a["name"] for a in ANIMALS if a != animal], 3)
        options = names + [animal["name"]]
        random.Random(self.round_index + 20).shuffle(options)
        for i, name in enumerate(options):
            self.add_button((120+i*180, 400, 160, 65), name,
                            [(255, 184, 77), (94, 195, 162), (107, 158, 238), (222, 129, 193)][i],
                            ("answer", name == animal["name"]))

    def feeder(self):
        animal = self.feeder_order[self.round_index]
        self.draw_panel("ماذا يأكل هذا الحيوان؟")
        self.progress.value = self.round_index
        self.progress.draw(self.screen)
        draw_animal(self.screen, animal["name"], (WIDTH//2, 265), 0.95, pygame.time.get_ticks()/1000)
        self.text(self.screen, f"أنا {animal['name']}، اختر نوع غذائي!", (WIDTH//2, 135), 27)
        colors = [(94, 195, 162), (255, 147, 120), (106, 158, 238)]
        for i, diet in enumerate(DIETS):
            self.add_button((190+i*205, 405, 180, 68), diet, colors[i],
                            ("answer", diet == animal["diet"]))

    def trivia(self):
        q = self.trivia_order[self.round_index]
        self.draw_panel("أسئلة العلماء")
        self.progress.value = self.round_index
        self.progress.draw(self.screen)
        self.text(self.screen, q["q"], (WIDTH//2, 155), 29)
        for i, option in enumerate(q["options"]):
            self.add_button((220, 225+i*72, 520, 57), option,
                            [(255, 190, 84), (107, 166, 239), (94, 195, 162)][i],
                            ("trivia", i == q["a"]))

    def leaderboard_screen(self):
        self.draw_panel("لوحة الأبطال")
        self.text(self.screen, "كل محاولة تعلّمنا شيئاً جديداً!", (WIDTH//2, 150), 27)
        rows = sorted(self.leaderboard, reverse=True)[:5]
        if not rows:
            self.text(self.screen, "ابدأ اللعب لتجمع النجوم!", (WIDTH//2, 250), 28)
        for i, score in enumerate(rows):
            self.text(self.screen, f"{i+1}. {score} نجمة", (WIDTH//2, 220+i*48), 27)
        self.add_button((380, 415, 200, 65), "عودة", (255, 184, 77), ("back", None))

    def finish_round(self, correct):
        if correct:
            self.score += 1
            self.stars.extend(FloatingStar(random.randint(250, 710), 250) for _ in range(7))
            self.confetti.append(Confetti(WIDTH//2, 230))
            self.message = "إجابة رائعة! أحسنت!"
        else:
            self.message = "محاولة جميلة! لنتعلم معاً."
        self.message_timer = 1.0
        self.round_index += 1
        length = {
            "identify": len(ANIMALS),
            "feeder": len(ANIMALS),
            "trivia": len(TRIVIA),
        }.get(self.state, 0)
        if self.round_index >= length:
            self.leaderboard.append(self.score)
            self.state = "menu"
            self.previous = ["menu"]

    def handle_action(self, action):
        kind, value = action
        if kind == "go":
            self.go(value)
        elif kind == "back":
            self.back()
        elif kind == "answer":
            self.finish_round(value)
        elif kind == "trivia":
            self.finish_round(value)

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(60)/1000.0, 0.05)
            size = self.screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, getattr(pygame, "K_AC_BACK", pygame.K_ESCAPE)
                ):
                    self.back()
                kind, pos = self.touch.events(event, size)
                if kind == "up" and pos:
                    sx, sy = WIDTH/size[0], HEIGHT/size[1]
                    logical = (int(pos[0]*sx), int(pos[1]*sy))
                    for button, action in list(self.buttons):
                        if button.contains(logical):
                            self.handle_action(action)
                            break

            self.screen = pygame.display.get_surface()
            self.screen.fill((130, 210, 255))
            self.buttons = []
            if self.state == "menu":
                self.menu()
            elif self.state == "identify":
                self.identify()
            elif self.state == "feeder":
                self.feeder()
            elif self.state == "trivia":
                self.trivia()
            elif self.state == "leaderboard":
                self.leaderboard_screen()

            for star in self.stars:
                star.update(dt)
                star.draw(self.screen)
            self.stars = [s for s in self.stars if s.life > 0]
            for burst in self.confetti:
                burst.update(dt)
                burst.draw(self.screen)
            self.confetti = [c for c in self.confetti if any(p[4] > 0 for p in c.particles)]

            if self.message_timer > 0:
                self.message_timer -= dt
                self.text(self.screen, self.message, (WIDTH//2, HEIGHT-55), 26, (60, 150, 102))

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    ScienceGame().run()
