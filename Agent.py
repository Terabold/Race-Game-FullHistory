import pygame
import math
from utils import blit_rotate_center

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
        self.vel = -self.vel * 1.05

    def drivesound(self, assets):
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        
        if self.vel > 3 and not self.drive_sound_playing:  # Start playing sound when velocity exceeds 3
            if current_time >= self.sound_start_time:  # Check if we've reached 2 seconds
                assets['drive'].play(loops=-1, start=2)  # Start the sound from the 2-second mark and loop it
                self.drive_sound_playing = True  # Mark the sound as playing
        elif self.vel <= 3 and self.drive_sound_playing:  # Stop the sound if velocity goes below 3
            assets['drive'].stop()
            self.drive_sound_playing = False


    def bounceextra(self):
        self.vel = -self.vel * 1.3 

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def set_image(self, img):
        self.img = img
