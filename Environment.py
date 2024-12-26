import pygame
import time

class Environment:
    def __init__(self, track, track_border, finish_line, finish_line_position):
        self.track = track
        self.track_border = track_border
        self.track_border_mask = pygame.mask.from_surface(track_border)
        self.finish_line = finish_line
        self.finish_line_position = finish_line_position
        self.finish_mask = pygame.mask.from_surface(finish_line)
        self.start_time = None
        self.font = pygame.font.Font(r'fonts\PressStart2P-Regular.ttf', 100)

        
    def setup_images(self, grass, track):
        self.images = [
            (grass, (0, 0)),
            (track, (0, 0)),
            (self.finish_line, self.finish_line_position),
            (self.track_border, (0, 0))
        ]
        return self.images

    def check_collision(self, car):
        return car.collide(self.track_border_mask)

    def check_finish(self, car):
        return car.collide(self.finish_mask, *self.finish_line_position)
