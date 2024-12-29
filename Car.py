import math
from Constants import *
import pygame

class Car(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.img = pygame.image.load(CAR_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.img, (20, 40))
        self.x, self.y = CAR_START_POS
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.max_velocity = CARSPEED
        self.velocity = 0
        self.rotation_velocity = ROTATESPEED
        self.angle = 0
        self.acceleration = ACCELERATION

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity

    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.move()

    def move_backward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.max_velocity / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        self.y -= vertical
        self.x -= horizontal

    def action(self, action):
        if action == 1:
            self.move_forward()
        if action == 2:
            self.move_backward()
        if action == 3:
            self.rotate(left=True)
        if action == 4:
            self.rotate(right=True)

    def reduce_speed(self):
        if self.velocity > 0:
            self.velocity = max(self.velocity - self.acceleration * 0.5, 0)  # Slow down more gently
        elif self.velocity < 0:
            self.velocity = min(self.velocity + self.acceleration * 0.5, 0)
        self.move()

    def handle_border_collision(self):
        # Determine if we're going forward or backward
        is_reversing = self.velocity < 0
        
        # Reduce and reverse velocity based on impact
        self.velocity *= -0.5  # Common practice to bounce back at reduced speed
        
        # Move car away from border - adjust direction based on forward/reverse
        radians = math.radians(self.angle)
        push_direction = -1 if is_reversing else 1  # Flip push direction when reversing
        
        self.x += math.sin(radians) * 10 * push_direction
        self.y += math.cos(radians) * 10 * push_direction
        
        # Reduce car's speed to create impact feel
        if abs(self.velocity) > 2:  # Only slow down significantly on hard impacts
            self.velocity *= 0.7
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = CAR_START_POS
        self.angle = 0
        self.velocity = 0

