import math
import pygame
from Constants import *
import numpy as np

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_color="Red") -> None:  # Modified to accept car_color
        super().__init__()
        self.x = x
        self.y = y
        # Use car color from CAR_COLORS dictionary in Constants.py
        self.img = pygame.image.load(CAR_COLORS[car_color]).convert_alpha()
        self.image = pygame.transform.scale(self.img, (19, 38))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.max_velocity = MAXSPEED
        self.velocity = 0
        self.rotation_velocity = ROTATESPEED
        self.angle = 0
        self.acceleration = ACCELERATION
        
        # Drift attributes
        self.drift_momentum = 0
        self.drift_friction = 0.87
        self.drift_factor = 0.1

        # Collision attributes
        self.recovery_bounce = 1.5
        self.recovery_slowdown = 0.6
        self.recovery_straighten = 5

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
            if abs(self.velocity) > self.max_velocity * 0.5:
                self.drift_momentum -= self.velocity * self.drift_factor
        elif right:
            self.angle -= self.rotation_velocity
            if abs(self.velocity) > self.max_velocity * 0.5:
                self.drift_momentum += self.velocity * self.drift_factor

    def move(self):
        # Combine movement calculations
        base_angle = math.radians(self.angle)
        drift_angle = base_angle + math.pi/2  # 90 degrees in radians
        
        # Calculate all movements at once
        total_vertical = (math.cos(base_angle) * self.velocity + 
                         math.cos(drift_angle) * self.drift_momentum)
        total_horizontal = (math.sin(base_angle) * self.velocity + 
                          math.sin(drift_angle) * self.drift_momentum)
        
        self.y -= total_vertical
        self.x -= total_horizontal
        self.drift_momentum *= self.drift_friction

    def accelerate(self, forward=True):
        if forward:
            self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        else:
            self.velocity = max(self.velocity - self.acceleration, -self.max_velocity / 2)
        self.move()

    def reduce_speed(self):
        if self.velocity > 0:
            self.velocity = max(self.velocity - self.acceleration * 0.3, 0)
        elif self.velocity < 0:
            self.velocity = min(self.velocity + self.acceleration * 0.3, 0)
        self.move()
        
    def reset(self, x=None, y=None):
        """Reset car state with optional new position"""
        if x is not None and y is not None:
            self.x = x
            self.y = y
        self.velocity = 0
        self.angle = 0
        self.drift_momentum = 0
        self.rect.center = (self.x, self.y)

    def handle_border_collision(self):
        # Store original position and movement to calculate the collision response
        original_x, original_y = self.x, self.y
        radians = math.radians(self.angle)
        
        # Calculate total movement
        drift_radians = math.radians(self.angle + 90)
        total_x = -(math.sin(radians) * self.velocity + 
                   math.sin(drift_radians) * self.drift_momentum)
        total_y = -(math.cos(radians) * self.velocity + 
                   math.cos(drift_radians) * self.drift_momentum)
        
        # Apply collision physics
        self.x = original_x - total_x * self.recovery_bounce
        self.y = original_y - total_y * self.recovery_bounce
        self.velocity *= -self.recovery_slowdown
        self.drift_momentum *= -self.recovery_slowdown
        
        if abs(self.velocity) > 1:
            movement_angle = math.degrees(math.atan2(-total_y, -total_x))
            current_angle = self.angle % 360
            movement_angle = movement_angle % 360
            angle_diff = ((movement_angle - current_angle + 180) % 360) - 180
            self.angle += angle_diff * 0.2
        
        # Cap speeds
        self.velocity = max(min(self.velocity, self.max_velocity), -self.max_velocity/2)
        self.drift_momentum = max(min(self.drift_momentum, self.max_velocity), -self.max_velocity)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(car_mask, offset)