import pygame

from .locals import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.w}, {self.h})'

    def contains(self, point):
        return self.x <= point.x < self.x + self.w and self.y <= point.y < self.y + self.h

    def intersects(self, other):
        return self.x < other.x + other.w\
                and self.x + self.w > other.x\
                and self.y < other.y + other.h\
                and self.y + self.h > other.y\

    def split(self):
        return (Rect(self.x, self.y, self.w / 2, self.h / 2),
                Rect(self.x + self.w / 2, self.y, self.w / 2, self.h / 2),
                Rect(self.x, self.y + self.h // 2, self.w / 2, self.h / 2),
                Rect(self.x + self.w / 2, self.y + self.h / 2, self.w / 2, self.h / 2))

class Quad:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        ne, nw, se, sw = self.boundary.split()

        self.q1 = Quad(ne, self.capacity)
        self.q2 = Quad(nw, self.capacity)
        self.q3 = Quad(se, self.capacity)
        self.q4 = Quad(sw, self.capacity)

        self.divided = True

    def insert(self, point):

        if not self.boundary.contains(point):
            return False

        elif len(self.points) < self.capacity-1:
            self.points.append(point)
            return True

        else:
            if not self.divided:
                self.subdivide()
            if self.q1.insert(point):
                return True
            elif self.q2.insert(point):
                return True
            elif self.q3.insert(point):
                return True
            elif self.q4.insert(point):
                return True
            return False

    def query(self, rect):
        results = []
        if not self.boundary.intersects(rect):
            return results

        for p in self.points:
            if rect.contains(p):
                results.append(p)

        if self.divided:
            results += self.q1.query(rect)
            results += self.q2.query(rect)
            results += self.q3.query(rect)
            results += self.q4.query(rect)

        return results

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, pygame.Rect((self.boundary.x * CELL_WIDTH, self.boundary.y * CELL_HEIGHT), (self.boundary.w * CELL_WIDTH, self.boundary.h * CELL_HEIGHT)), 1)
        if self.divided:
            self.q1.draw(surface, color)
            self.q2.draw(surface, color)
            self.q3.draw(surface, color)
            self.q4.draw(surface, color)
