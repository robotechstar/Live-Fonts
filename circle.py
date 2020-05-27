import pygame
from conf import *
import random

vec = pygame.math.Vector2


class Circle:
    def __init__(self, screen, pos, colour):
        self.spawn = vec(pos)  # This is the disignated position of the circle when called
        # This is the currect position of the circle
        if random.random() < 0.1:
            self.pos = vec(random.randrange(WIDTH), random.randrange(HEIGHT))
        else:
            self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.screen = screen
        self.radius = STARTING_RADIUS
        self.colour = colour
        self.growing = True

    def check_boundary(self):
        if (self.spawn.x - self.radius - 1 < 0) or (self.spawn.x + self.radius + 1 > WIDTH):
            self.growing = False
        if (self.spawn.y - self.radius - 1 < 0) or (self.spawn.y + self.radius + 1 > HEIGHT):
            self.growing = False

    def arrive(self):
        self.vel = self.spawn - self.pos
        d = self.vel.length()
        if PARKING_DIST > d > 1:
            self.vel.scale_to_length(d * 0.1)
        elif d > PARKING_DIST:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel

    def flee(self, desired):
        desired.normalize()
        desired *= MAX_SPEED
        steer = desired - self.vel
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        self.vel += steer
        self.pos += self.vel

    def move(self, target):
        desired = self.pos - target
        if desired.length() < MOUSE_RANGE + random.randrange(-10, 10):
            self.flee(desired)
        else:
            self.arrive()

    def grow(self):
        if self.growing and self.radius < 10:
            self.radius += 1

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, (int(self.pos.x), int(self.pos.y)), self.radius)
