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
        
    def setup_images(self, grass, track):
        self.images = [
            (grass, (0, 0)),
            (track, (0, 0)),
            (self.finish_line, self.finish_line_position),
            (self.track_border, (0, 0))
        ]
        return self.images
    
    def draw(self, game, images, car):
        for img, pos in images:
            game.blit(img, pos)
        car.draw(game)

    def check_collision(self, car):
        return car.collide(self.track_border_mask)

    def check_finish(self, car):
        return car.collide(self.finish_mask, *self.finish_line_position)

    def countdown(self, game, car, images):
        font = pygame.font.Font(None, 100)
        car.reset()
        
        for i in range(3, 0, -1):
            self.draw(game, images, car)
            text = font.render(str(i), True, (255, 255, 255))
            text_rect = text.get_rect(center=(game.get_width() // 2, game.get_height() // 2))
            game.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(1000)
        
        self.start_time = time.time()