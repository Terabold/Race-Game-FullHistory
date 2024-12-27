import pygame
import math
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

    def handle_border_collision(self):
        # Determine if we're going forward or backward
        is_reversing = self.vel < 0
        
        # Reduce and reverse velocity based on impact
        self.vel *= -0.5  # Common practice to bounce back at reduced speed
        
        # Move car away from border - adjust direction based on forward/reverse
        radians = math.radians(self.angle)
        push_direction = -1 if is_reversing else 1  # Flip push direction when reversing
        
        self.x += math.sin(radians) * 10 * push_direction
        self.y += math.cos(radians) * 10 * push_direction
        
        # Reduce car's speed to create impact feel
        if abs(self.vel) > 2:  # Only slow down significantly on hard impacts
            self.vel *= 0.7

    def handle_finishline_collision(self):
        self.vel *= -1.3
    
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
