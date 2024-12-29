import math
import pygame
from Constants import *

class Speedometer:
    def __init__(self):
        self.font = pygame.font.Font(FONT, 30)  # Increased font size
        self.needle_color = (255, 0, 0)
        self.center = (150, HEIGHT - 150)  # Moved position
        self.radius = 70  # Increased radius
        
    def draw(self, surface, velocity):
        # Draw speedometer background
        pygame.draw.circle(surface, WHITE, self.center, self.radius, 3)  # Thicker circle
        
        # Draw tick marks
        for i in range(7):  # 6 sections
            angle = math.radians(180 - (i * 30))  # 180 degrees divided into 6 parts
            start_x = self.center[0] + math.cos(angle) * (self.radius - 10)
            start_y = self.center[1] - math.sin(angle) * (self.radius - 10)
            end_x = self.center[0] + math.cos(angle) * self.radius
            end_y = self.center[1] - math.sin(angle) * self.radius
            pygame.draw.line(surface, WHITE, (start_x, start_y), (end_x, end_y), 2)
        
        # Convert velocity to angle (180 to 0 degrees for left to right movement)
        speed_percent = abs(velocity) / CARSPEED
        angle = 180 - (180 * speed_percent)
        angle_rad = math.radians(angle)
        
        # Draw needle with a thicker line
        end_x = self.center[0] + math.cos(angle_rad) * (self.radius - 10)
        end_y = self.center[1] - math.sin(angle_rad) * (self.radius - 10)
        pygame.draw.line(surface, self.needle_color, self.center, (end_x, end_y), 3)
        
        # Draw center cap of needle
        pygame.draw.circle(surface, self.needle_color, self.center, 5)
        
        # Draw speed text in center-bottom of speedometer
        speed_text = self.font.render(f"{abs(velocity*25):.1f} Km/h", True, WHITE)
        text_rect = speed_text.get_rect(center=(self.center[0], self.center[1] + self.radius + 20))
        surface.blit(speed_text, text_rect)