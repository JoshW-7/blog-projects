import pygame
import random
import numpy as np


class Obstacle:
    def __init__(self, x, y, color=(255, 0, 0), size=10):
        self.pos = np.array([0, 0], dtype=float)
        self.color = color
        self.size = size

    def update(self, window):
        x, y = pygame.mouse.get_pos()
        self.pos[0] = x
        self.pos[1] = y

    def draw(self, window):
        pygame.draw.circle(window.screen, self.color, (self.pos[0], self.pos[1]), self.size)


class Boid:
    alignment = True                  # Whether the rule of alignment is enabled
    cohesion = True                   # Whether the rule of cohesion is enabled
    separation = True                 # Whether the rule of separation is enabled
    separation_factor = 0.01          # How much to avoid other boids
    distance_max_visibility = 100     # How far away a boid can see other boids
    trail_length = 50

    def __init__(self, x, y, color=(255, 255, 255), size=10):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.speed = 2
        self.color = color
        self.size = size
        self.pos_avg = np.array([0, 0], dtype=float)
        self.vel_avg = np.array([0, 0], dtype=float)
        self.cohesion_direction = np.array([0, 0], dtype=float)
        self.separation_direction = np.array([0, 0], dtype=float)
        self.last_positions = []

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @y.setter
    def y(self, value):
        self.pos[1] = value

    def distance_to_entity(self, entity):
        return np.linalg.norm(self.pos - entity.pos)

    def get_local_entities(self, objects, entity_type):
        local_entities = []
        for obj in objects:
            if obj is not self and isinstance(obj, entity_type):
                if self.distance_to_entity(obj) < Boid.distance_max_visibility:
                    local_entities.append(obj)
        return local_entities

    def update(self, window):
        self.last_positions.append(np.array([self.pos[0], self.pos[1]], dtype=float))
        if len(self.last_positions) > Boid.trail_length:
            self.last_positions.pop(0)
        self.pos_avg = np.array([0, 0], dtype=float)
        self.vel_avg = np.array([0, 0], dtype=float)
        self.acc = np.array([0, 0], dtype=float)
        self.separation_direction = np.array([0, 0], dtype=float)

        # Get all the other boids within range
        local_boids = self.get_local_entities(window.objects, Boid)

        # Calculate local boids' average position and velocity
        n_boids = len(local_boids)
        if n_boids > 0:
            self.pos_avg = sum([boid.pos for boid in local_boids]) / n_boids
            self.vel_avg = sum([boid.vel for boid in local_boids]) / n_boids
            self.vel_avg /= np.linalg.norm(self.vel_avg)
            self.cohesion_direction = self.pos_avg - self.pos
            self.cohesion_direction /= np.linalg.norm(self.cohesion_direction)

        # Rule of cohesion
        if Boid.cohesion:
            if self.pos[0] < self.pos_avg[0]:
                self.acc[0] += 0.02
            elif self.pos[0] > self.pos_avg[0]:
                self.acc[0] -= 0.02
            if self.pos[1] < self.pos_avg[1]:
                self.acc[1] += 0.02
            elif self.pos[1] > self.pos_avg[1]:
                self.acc[1] -= 0.02

        # Rule of alignment
        if Boid.alignment:
            if self.vel[0] < self.vel_avg[0]:
                self.acc[0] += 0.01
            elif self.vel[0] > self.vel_avg[0]:
                self.acc[0] -= 0.01
            if self.vel[1] < self.vel_avg[1]:
                self.acc[1] += 0.01
            elif self.vel[1] > self.vel_avg[1]:
                self.acc[1] -= 0.01

        # Rule of separation
        if Boid.separation:
            for boid in local_boids:
                diff = self.pos - boid.pos
                diff /= (self.distance_to_entity(boid) / Boid.separation_factor)
                self.separation_direction += diff
            self.acc += self.separation_direction

        # Avoid external obstacles
        local_obstacles = self.get_local_entities(window.objects, Obstacle)
        n_obstacles = len(local_obstacles)
        if n_obstacles > 0:
            for obstacle in local_obstacles:
                diff = self.pos - obstacle.pos
                diff /= (self.distance_to_entity(obstacle) / (Boid.separation_factor * 5))
                self.separation_direction += diff
            self.acc += self.separation_direction

        # Accumulate acceleration into velocity and velocity into position
        self.vel += self.acc
        if (magnitude := np.linalg.norm(self.vel)) > self.speed:
            self.vel /= magnitude
        self.pos += self.vel * self.speed

        # Wrap horizontally
        if self.x > window.width:
            self.x = self.x - window.width
        elif self.x < 0:
            self.x = window.width + self.x

        # Wrap vertically
        if self.y > window.height:
            self.y = self.y - window.height
        elif self.y < 0:
            self.y = window.height + self.y

    def draw(self, window):
        # Draw this boid
        pygame.draw.circle(window.screen, self.color, (self.x, self.y), self.size)

        # Draw this boid's velocity vector as a red line
        # pygame.draw.line(window.screen, (255, 0, 0), (self.x, self.y), (self.x + self.vel[0]*20/np.linalg.norm(self.vel), self.y + self.vel[1]*20/np.linalg.norm(self.vel)), 2)

        # Draw the local boids' average velocity vector as a green line
        # pygame.draw.line(window.screen, (0, 255, 0), (self.x, self.y), (self.x + self.vel_avg[0] * 20, self.y + self.vel_avg[1] * 20), 2)

        # Draw the local boids' average position as a blue circle
        # pygame.draw.circle(window.screen, (0, 0, 255), (self.pos_avg[0], self.pos_avg[1]), 3)

        # Draw the last positions
        for pos in self.last_positions:
            pygame.draw.circle(window.screen, (0, 0, 255), (pos[0], pos[1]), 1)