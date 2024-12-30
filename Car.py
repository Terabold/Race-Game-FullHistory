import math
from Constants import *
import pygame
class Car(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.img = pygame.image.load(CAR_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.img, (19, 38))
        self.x, self.y = CAR_START_POS
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.max_velocity = CARSPEED
        self.velocity = 0
        self.rotation_velocity = ROTATESPEED
        self.angle = 0
        self.acceleration = ACCELERATION
        
        # New drift-related attributes
        self.drift_momentum = 0
        self.drift_friction = 0.87  # How quickly drift momentum decays
        self.drift_factor = 0.1   # How much turning affects drift

        # Collision recovery attributes
        self.recovery_bounce = 1.5  # How much the car bounces off walls
        self.recovery_slowdown = 0.6 # How much to slow down on collision
        self.recovery_straighten = 13  # How much to straighten car on collision

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
            # Add drift momentum when turning at speed
            if abs(self.velocity) > self.max_velocity * 0.5:
                self.drift_momentum -= self.velocity * self.drift_factor
        elif right:
            self.angle -= self.rotation_velocity
            # Add drift momentum when turning at speed
            if abs(self.velocity) > self.max_velocity * 0.5:
                self.drift_momentum += self.velocity * self.drift_factor

    def move(self):
        # Calculate regular movement
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        
        # Calculate drift movement (perpendicular to car's direction)
        drift_radians = math.radians(self.angle + 90)
        drift_vertical = math.cos(drift_radians) * self.drift_momentum
        drift_horizontal = math.sin(drift_radians) * self.drift_momentum
        
        # Combine regular movement and drift
        self.y -= (vertical + drift_vertical)
        self.x -= (horizontal + drift_horizontal)
        
        # Apply drift friction
        self.drift_momentum *= self.drift_friction

    def reset(self):
        self.x, self.y = CAR_START_POS
        self.angle = 0
        self.velocity = 0
        self.drift_momentum = 0  # Reset drift momentum

    # Rest of the methods remain unchanged
    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.move()

    def move_backward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.max_velocity / 2)
        self.move()

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
            self.velocity = max(self.velocity - self.acceleration * 0.3, 0)
        elif self.velocity < 0:
            self.velocity = min(self.velocity + self.acceleration * 0.3, 0)
        self.move()


    def handle_border_collision(self):
        # Store original position and movement
        original_x, original_y = self.x, self.y
        radians = math.radians(self.angle)
        
        # Calculate total movement vector (including drift)
        drift_radians = math.radians(self.angle + 90)
        total_x = -(math.sin(radians) * self.velocity + 
                   math.sin(drift_radians) * self.drift_momentum)
        total_y = -(math.cos(radians) * self.velocity + 
                   math.cos(drift_radians) * self.drift_momentum)
        
        # Reverse movement direction with dampening
        self.x = original_x - total_x * self.recovery_bounce
        self.y = original_y - total_y * self.recovery_bounce
        
        # Reduce speed and drift
        self.velocity *= -self.recovery_slowdown
        self.drift_momentum *= -self.recovery_slowdown
        
        # Straighten car slightly towards the opposite direction
        if abs(self.velocity) > 1:
            # Calculate angle to movement direction
            movement_angle = math.degrees(math.atan2(-total_y, -total_x))
            # Normalize angles
            current_angle = self.angle % 360
            movement_angle = movement_angle % 360
            
            # Calculate shortest rotation direction
            angle_diff = ((movement_angle - current_angle + 180) % 360) - 180
            
            # Apply partial straightening
            self.angle += angle_diff * 0.2  # Gradual straightening factor
        
        # Ensure speed caps
        self.velocity = max(min(self.velocity, self.max_velocity), -self.max_velocity/2)
        self.drift_momentum = max(min(self.drift_momentum, self.max_velocity), -self.max_velocity)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi