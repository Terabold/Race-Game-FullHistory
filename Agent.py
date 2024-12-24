import pygame
import math
import time
class Car:
    START_POS = (350, 200)

    def __init__(self, max_vel, rotation_vel):
        self.img = None  # Will be set in main.py
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.12
        self.collide_count = 0  # Track number of collisions


    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration * 0.3, 0)  # Slow down more gently
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration * 0.3, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 4  # Normal bounce (stronger effect)
        time.sleep(0.01)
        self.vel *= 0.2  # Reduce speed (damping)

    def bounceextra(self):
        self.vel = -self.vel * 1.3 

    def check_restart(self):
        if self.collide_count > 400:  
            return True  
        return False
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        if poi: 
            self.collide_count += 1
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def set_image(self, img):
        self.img = img
