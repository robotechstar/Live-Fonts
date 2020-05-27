import pygame
import os
from conf import *
from circle import *
import random
from pygame_widgets import TextBox

# Inintialize
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Live Fonts')
clock = pygame.time.Clock()
circles = []


def add_circle():
    # spawn_point = (random.randrange(WIDTH), random.randrange(HEIGHT))
    spawn_point = random.choice(spawn_points)
    space_free = True
    for circle0 in circles:
        if ((circle0.spawn.x - spawn_point[0]) ** 2) + (
                (circle0.spawn.y - spawn_point[1]) ** 2) < circle0.radius ** 2 + 2:
            space_free = False
            break
    if space_free:
        colour = random.choice(COLOURS)
        circles.append(Circle(screen, spawn_point, colour))
    for circle0 in circles:
        for circle1 in circles:
            if circle1 == circle0:
                continue
            if (circle1.spawn - circle0.spawn).length() < circle0.radius + circle1.radius + 2:
                circle0.growing = False
                break


spawn_points = []


def draw_text(text0, colour, x, y):
    text = text0.upper().replace('', ' ')
    size = WIDTH // len(text) * 3
    font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = font.render(text, 1, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def ask():
    screen.fill(BLACK)
    text_box = TextBox(screen, (WIDTH // 2) - 250, (HEIGHT // 2) - 50, 500, 100, fontSize=75, borderColour=BLACK,
                       textColour=BLACK)
    waiting = True
    while waiting:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

        text_box.listen(events)
        text_box.draw()
        if not waiting:
            screen.fill(BLACK)
            draw_text(text_box.getText(), WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
    del text_box


def scan():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            pix = screen.get_at((x, y))[:3]
            if pix == (255, 255, 255):
                spawn_points.append((x, y))


def run():
    running = True
    while running:
        clock.tick(30)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for circle in circles:
                    circle.pos = vec((random.randrange(WIDTH), random.randrange(HEIGHT)))
        mouse = pygame.mouse.get_pos()

        add_circle()

        for circle in circles:
            circle.check_boundary()
            circle.grow()
            circle.move(mouse)
            circle.draw()
        pygame.display.flip()
    for circle in circles:
        circles.remove(circle)


while True:
    ask()
    scan()
    run()
