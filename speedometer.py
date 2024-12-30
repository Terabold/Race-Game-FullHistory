import math
from typing import Tuple
import pygame
from Constants import FONT, HEIGHT, WHITE, CARSPEED

class Speedometer:
    def __init__(self):
        self.font = pygame.font.Font(FONT, 30)
        self.needle_color = (255, 0, 0)
        self.center = (150, HEIGHT - 150)
        self.radius = 70
        self.tick_angles = [math.radians(180 - (i * 30)) for i in range(7)]
        
    def _calculate_tick_positions(self, angle: float) -> Tuple[float, float, float, float]:
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        start_x = self.center[0] + cos_angle * (self.radius - 10)
        start_y = self.center[1] - sin_angle * (self.radius - 10)
        end_x = self.center[0] + cos_angle * self.radius
        end_y = self.center[1] - sin_angle * self.radius
        return start_x, start_y, end_x, end_y
    
    def draw(self, surface: pygame.Surface, velocity: float) -> None:
        # Draw background
        pygame.draw.circle(surface, WHITE, self.center, self.radius, 3)
        
        # Draw tick marks
        for angle in self.tick_angles:
            start_x, start_y, end_x, end_y = self._calculate_tick_positions(angle)
            pygame.draw.line(surface, WHITE, (start_x, start_y), (end_x, end_y), 2)
        
        # Calculate and draw needle
        speed_percent = abs(velocity) / CARSPEED
        angle_rad = math.radians(180 - (180 * speed_percent))
        needle_end = (
            self.center[0] + math.cos(angle_rad) * (self.radius - 10),
            self.center[1] - math.sin(angle_rad) * (self.radius - 10)
        )
        pygame.draw.line(surface, self.needle_color, self.center, needle_end, 3)
        pygame.draw.circle(surface, self.needle_color, self.center, 5)
        
        # Draw speed text
        speed_text = self.font.render(f"{abs(velocity*28):.0f} Km/h", True, WHITE)
        text_rect = speed_text.get_rect(center=(self.center[0], self.center[1] + self.radius + 20))
        surface.blit(speed_text, text_rect)