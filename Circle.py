import pygame
import numpy as np
from random import randint
from itertools import combinations

FIELD_WIDTH = 600
FIELD_HEIGHT = 600
id_list = []

class Circle:
    VELOCITY_MAX = 3

    def __init__(self):
        self.id = len(self.id_list) + 1
        self.id_list.append(self.id)
        self.mass = randint(10, 100)
        self.radius = randint(10, 40)
        self.r = np.array((randint(0 + self.radius, FIELD_WIDTH - self.radius),
                                               randint(0 + self.radius, FIELD_HEIGHT - self.radius)))
        self.v = np.array((randint(-self.VELOCITY_MAX, self.VELOCITY_MAX), randint(-self.VELOCITY_MAX, self.VELOCITY_MAX)))
        if self.v[0] == 0 or self.v[1] == 0:
            self.v = pygame.math.Vector2(randint(-self.VELOCITY_MAX, self.VELOCITY_MAX), randint(-self.VELOCITY_MAX, self.VELOCITY_MAX))
        self.a = np.array((1,1))
        self.color = (randint(10, 255), randint(10, 255), randint(10, 255))

    def draw(self, screen):
        self.screen = screen
        return pygame.draw.circle(self.screen, self.color, (self.r[0], self.r[1]), self.radius)

    def movement(self, dt):
        self.r[0] += self.v[0] * dt
        self.r[1] += self.v[1] * dt

    def update(self, dt):
        self.movement(dt)


class Simulation(Circle):
    def check_wall(self):
        if self.r[0] - self.radius < 0:
            self.r[0] = self.radius
            self.v[0] = -self.v[0]
        if self.r[0] + self.radius > FIELD_WIDTH:
            self.r[0] = 1 - self.radius
            self.v[0] = -self.v[0]
        if self.r[1] - self.radius < 0:
            self.r[1] = self.radius
            self.v[1] = -self.v[1]
        if self.r[1] + self.radius > FIELD_HEIGHT:
            self.r[1] = 1 - self.radius
            self.v[1] = -self.v[1]

    def overlaps(self, p2):
        return np.hypot(*(self.r - p2.r)) < self.radius + p2.radius # Wozu der Stern?

    def change_velocity(self, p2):
        r1 = self.r
        r2 = p2.r
        v1 = self.v
        v2 = p2.v
        m1 = self.mass
        m2 = p2.mass            # Woher die Masse?
        M = m1 + m2
        d = np.linalg.norm(r1 - r2) ** 2
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        self.v = u1
        p2.v = u2
        return self.v, p2.v



'''class Simulation(Circle):
    #def __init__(self):
     #   self.id_list = Circle.id_list

    def wall_collision(particle):
        if particle.r[0] - particle.radius < 0:
            particle.r[0] = particle.radius
            particle.v[0] = -particle.v[0]
        if particle.r[0] + particle.radius > 1:
            particle.r[0] = 1 - particle.radius
            particle.v[0] = -particle.v[0]
        if particle.r[1] - particle.radius < 0:
            particle.r[1] = particle.radius
            particle.v[1] = -particle.v[1]
        if particle.r[1] + particle.radius > 1:
            particle.r[1] = 1 - particle.radius
            particle.v[1] = -particle.v[1]


    def change_velocity(p1, p2):
        r1 = p1.r
        r2 = p2.r
        v1 = p1.v
        v2 = p2.v
        m1 = p1.mass
        m2 = p2.mass
        M = m1 + m2
        d = np.linalg.norm(r1 - r2) ** 2
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.v = u1
        p2.v = u2
        return p1.v, p2.v


    def circle_collision(p1, p2):
        pairs = combinations(range(len(Circle.id_list)), 2)
        for i, j in pairs:
            if p1.overlaps(p2):
                p1.change_velocity(p1, p2)

    def overlaps(self, p2):
        return np.hypot(*(self.r - p2.r)) < self.radius + p2.radius

    def is_clicked(self):
        pass'''