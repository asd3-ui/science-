"""Procedural animal illustrations. All artwork is drawn with pygame geometry."""
import math
import pygame

PALETTE = {
    "sky": (139, 213, 255),
    "cream": (255, 244, 204),
    "ink": (52, 58, 86),
}


def _ellipse(surface, color, rect, outline=None, width=1):
    pygame.draw.ellipse(surface, color, rect)
    if outline:
        pygame.draw.ellipse(surface, outline, rect, width)


def draw_animal(surface, animal, center, scale=1.0, t=0.0):
    """Draw one friendly animal centered at (x, y)."""
    x, y = center
    s = scale
    dark = (72, 58, 65)
    white = (255, 255, 255)
    blink = 0.35 if math.sin(t * 4.0) > 0.97 else 1.0

    if animal == "أسد":
        mane = (224, 123, 42)
        _ellipse(surface, (181, 86, 42), (x-93*s, y-90*s, 186*s, 184*s))
        _ellipse(surface, mane, (x-82*s, y-82*s, 164*s, 164*s))
        _ellipse(surface, (250, 205, 116), (x-56*s, y-49*s, 112*s, 108*s))
        _ellipse(surface, (255, 222, 145), (x-27*s, y+15*s, 54*s, 31*s))
        _ellipse(surface, dark, (x-31*s, y-20*s, 13*s, 13*s*blink))
        _ellipse(surface, dark, (x+18*s, y-20*s, 13*s, 13*s*blink))
        pygame.draw.polygon(surface, (91, 52, 57), [
            (x-8*s, y+1*s), (x+8*s, y+1*s), (x, y+10*s)])
        pygame.draw.arc(surface, dark, (x-14*s, y+5*s, 28*s, 22*s), 0, math.pi, 3)

    elif animal == "فيل":
        grey = (145, 170, 184)
        _ellipse(surface, grey, (x-77*s, y-66*s, 154*s, 132*s))
        _ellipse(surface, (119, 146, 163), (x-89*s, y-39*s, 65*s, 81*s))
        _ellipse(surface, (188, 205, 210), (x-78*s, y-52*s, 45*s, 61*s))
        pygame.draw.roundrect(surface, grey, (x+25*s, y-2*s, 34*s, 84*s), int(15*s))
        _ellipse(surface, (113, 139, 151), (x+24*s, y+60*s, 36*s, 20*s))
        _ellipse(surface, white, (x+31*s, y-31*s, 23*s, 29*s))
        _ellipse(surface, dark, (x+39*s, y-22*s, 9*s, 12*s*blink))
        pygame.draw.line(surface, white, (x+20*s, y+19*s), (x+37*s, y+42*s), max(2, int(5*s)))

    elif animal == "قرد":
        brown = (156, 94, 53)
        _ellipse(surface, brown, (x-66*s, y-65*s, 132*s, 128*s))
        _ellipse(surface, (242, 190, 128), (x-48*s, y-25*s, 96*s, 75*s))
        _ellipse(surface, (242, 190, 128), (x-77*s, y-48*s, 38*s, 42*s))
        _ellipse(surface, (255, 218, 168), (x-70*s, y-40*s, 25*s, 27*s))
        _ellipse(surface, (242, 190, 128), (x+39*s, y-48*s, 38*s, 42*s))
        _ellipse(surface, (255, 218, 168), (x+46*s, y-40*s, 25*s, 27*s))
        for ex in (-24, 24):
            _ellipse(surface, white, (x+ex*s-9*s, y-30*s, 18*s, 23*s))
            _ellipse(surface, dark, (x+ex*s-3*s, y-23*s, 8*s, 12*s*blink))
        _ellipse(surface, (100, 52, 46), (x-8*s, y+5*s, 16*s, 11*s))
        pygame.draw.arc(surface, dark, (x-19*s, y+14*s, 38*s, 20*s), 0, math.pi, 3)

    elif animal == "طائر":
        bob = math.sin(t*5)*3*s
        _ellipse(surface, (70, 166, 224), (x-59*s, y-43*s+bob, 118*s, 91*s))
        _ellipse(surface, (111, 199, 240), (x-20*s, y-25*s+bob, 67*s, 60*s))
        pygame.draw.polygon(surface, (255, 183, 61), [
            (x+45*s, y-8*s+bob), (x+78*s, y+2*s+bob), (x+45*s, y+12*s+bob)])
        _ellipse(surface, white, (x+15*s, y-27*s+bob, 28*s, 29*s))
        _ellipse(surface, dark, (x+25*s, y-19*s+bob, 11*s, 13*s*blink))
        pygame.draw.polygon(surface, (55, 134, 192), [
            (x-35*s, y+13*s+bob), (x+6*s, y+22*s+bob), (x-31*s, y+39*s+bob)])
        pygame.draw.line(surface, (115, 80, 51), (x-8*s, y+40*s), (x-8*s, y+53*s), 3)
        pygame.draw.line(surface, (115, 80, 51), (x+7*s, y+40*s), (x+7*s, y+53*s), 3)

    elif animal == "سمكة":
        bob = math.sin(t*4)*5*s
        pygame.draw.polygon(surface, (255, 173, 64), [
            (x-43*s, y+bob), (x-86*s, y-32*s+bob), (x-83*s, y+32*s+bob)])
        _ellipse(surface, (255, 128, 105), (x-58*s, y-39*s+bob, 116*s, 78*s))
        pygame.draw.polygon(surface, (255, 205, 95), [
            (x-14*s, y-34*s+bob), (x+11*s, y-59*s+bob), (x+29*s, y-28*s+bob)])
        _ellipse(surface, white, (x+22*s, y-19*s+bob, 24*s, 24*s))
        _ellipse(surface, dark, (x+31*s, y-12*s+bob, 9*s, 10*s*blink))
        pygame.draw.arc(surface, dark, (x+13*s, y+1*s+bob, 21*s, 16*s), 0, math.pi, 2)

    else:
        _ellipse(surface, (140, 190, 120), (x-48*s, y-45*s, 96*s, 90*s))


def draw_background(surface, t=0.0):
    surface.fill(PALETTE["sky"])
    w, h = surface.get_size()
    pygame.draw.circle(surface, (255, 226, 115), (w-85, 80), 42)
    pygame.draw.ellipse(surface, (117, 205, 151), (-70, h-100, w//2, 180))
    pygame.draw.ellipse(surface, (92, 185, 132), (w//3, h-65, w, 160))
    for i in range(6):
        cx = (i*193 + int(t*12)) % (w+100)
        pygame.draw.circle(surface, (255, 255, 255), (cx, 70+(i%3)*32), 4)
