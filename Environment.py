import pygame
from Car import Car
from Ground import Ground
from Constants import *
from speedometer import Speedometer

def font_scale(size):
    return pygame.font.Font(r'fonts\PressStart2P-Regular.ttf', size)

def blit_rotate_center(game, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(topleft = top_left).center)
    game.blit(rotated_image, new_rect.topleft)

class Environment:
    def __init__(self, surface) -> None:
        self.surface = surface
        
        # Track elements
        self.ground = Ground()
        self.ground_group = pygame.sprite.GroupSingle(self.ground)
        self.track_border = pygame.image.load(TRACKBORDER).convert_alpha()
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.finish_line = pygame.image.load(FINISHLINE).convert_alpha()
        self.finish_line = pygame.transform.scale(self.finish_line, (150, 25))
        self.finish_line_position = FINISHLINE_POSITION
        self.finish_mask = pygame.mask.from_surface(self.finish_line)
        
        # Sound
        self.setup_sound()
        
        # Game elements
        self.car = Car()
        self.car_group = pygame.sprite.GroupSingle(self.car)
        self.speedometer = Speedometer()
        self.elapsed_time = 0
        self.start_time = None

    def setup_sound(self):
        self.background_music = pygame.mixer.Sound(BACKGROUND_MUSIC)
        self.background_music.set_volume(0.01)
        self.countdown_sound = pygame.mixer.Sound(COUNTDOWN_SOUND)
        self.countdown_sound.set_volume(0.1)
        self.collide_sound = pygame.mixer.Sound(COLLIDE_SOUND)
        self.collide_sound.set_volume(4)
        self.win_sound = pygame.mixer.Sound(WIN_SOUND)
        self.win_sound.set_volume(0.2)
        self.is_music_playing = False

    def handle_music(self, play=True):
        if play and not self.is_music_playing:
            self.background_music.play(-1)
            self.is_music_playing = True
        elif not play:
            self.background_music.stop()
            self.is_music_playing = False

    def update_time(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def draw(self):
        self.ground_group.draw(self.surface)
        self.surface.blit(self.track_border, (0, 0))
        self.surface.blit(self.finish_line, self.finish_line_position)
        blit_rotate_center(self.surface, self.car.image, 
                          (self.car.x, self.car.y), self.car.angle)

    def draw_ui(self, clock):
        fps_text = font_scale(18).render(f"FPS: {int(clock.get_fps())}", True, WHITE)
        self.surface.blit(fps_text, (10, 10))

        if self.elapsed_time > 0:
            timer_text = font_scale(25).render(f"Time: {self.elapsed_time:.2f}", True, WHITE)
            self.surface.blit(timer_text, (10, self.surface.get_height() - 40))
            self.speedometer.draw(self.surface, self.car.velocity)

    def draw_countdown(self, count):
        # Shadow
        shadow = font_scale(125).render(str(count), True, FOGGRAY)
        shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surface.blit(shadow, (0, 0))
        shadow_surface.set_alpha(150)
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 2 + 5))
        
        # Main text
        text = font_scale(125).render(str(count), True, (220, 20, 60))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        self.surface.blit(shadow_surface, shadow_rect)
        self.surface.blit(text, text_rect)

    def draw_winner(self):   
        winner_text = font_scale(40).render(f"Time: {self.elapsed_time:.2f} sec", True, GOLD)
        restart_text = font_scale(40).render("Press SPACE to play again", True, GREEN)
        
        winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        
        self.surface.blit(winner_text, winner_rect)
        self.surface.blit(restart_text, restart_rect)

    def restart(self):
        self.elapsed_time = 0
        self.car.reset()
        self.start_time = None

    def check_collision(self):
        if collision := self.car.collide(self.track_border_mask):
            self.car.handle_border_collision()
            self.collide_sound.play()
        return collision

    def check_finish(self):
        if finish_pos := self.car.collide(self.finish_mask, *self.finish_line_position):
            if finish_pos[1] == 0:
                self.car.handle_border_collision()
            else:
                self.win_sound.play()
                return True
        return False

    def move(self):
        keys = pygame.key.get_pressed()
        moving = False

        # Handle movement
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.car.accelerate(True)
            moving = True
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.car.accelerate(False)
            moving = True

        # Handle rotation
        if keys[pygame.K_a]: 
            self.car.rotate(left=True)
        if keys[pygame.K_d]:  
            self.car.rotate(right=True)

        if not moving:
            self.car.reduce_speed()

        # Check collisions and finish
        self.check_collision()
        return self.check_finish()