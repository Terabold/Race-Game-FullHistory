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
        font = r'fonts\PressStart2P-Regular.ttf'
        font = pygame.font.Font(font, 100)
        car.reset()

        for i in range(3, 0, -1):
            self.draw(game, images, car)
            
            # Render foggy shadow (slightly offset)
            shadow = font.render(str(i), True, (50, 50, 50))  # Fog-like gray shadow
            shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
            shadow_surface.blit(shadow, (0, 0))
            shadow_surface.set_alpha(150)  # Make the shadow semi-transparent
            shadow_rect = shadow_surface.get_rect(center=(game.get_width() // 2 + 5, game.get_height() // 2 + 5))
            
            # Render the main text
            text_color = (220, 20, 60)  # Gradually fade from white to light blue
            text = font.render(str(i), True, text_color)
            text_rect = text.get_rect(center=(game.get_width() // 2, game.get_height() // 2))
            
            # Draw the shadow and the main text
            game.blit(shadow_surface, shadow_rect)
            game.blit(text, text_rect)
            
            pygame.display.update()
            pygame.time.wait(800)

        self.start_time = time.time()