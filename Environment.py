import torch
import numpy as np
import pygame
from Constants import *
from Car import Car
from Ground import Ground
import time

def font_scale(size, Font=FONT):
    return pygame.font.Font(Font, size)

def blit_rotate_center(game, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    game.blit(rotated_image, new_rect.topleft)

class Environment:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.ground_group = pygame.sprite.GroupSingle(Ground())
        self.current_level = 0
        
        # Initialize car with starting position from the first level
        start_pos = LEVELS[0]["car_start_pos"]
        self.car = Car(*start_pos)
        self.car_group = pygame.sprite.GroupSingle(self.car)
        
        # Initialize the first level
        self.load_level(self.current_level)
        
        # Initialize sound and timer
        self.setup_sound()
        self.remaining_time = LEVELS[0]["target_time"]  # Set the timer for the first level
        self.game_state = "running"
        
    def load_level(self, level_index):
        level_data = LEVELS[level_index]
        self.current_level_data = level_data
        
        # Load track and border
        self.track = pygame.image.load(level_data["track_image"]).convert_alpha()
        self.track_border = pygame.image.load(level_data["border_image"]).convert_alpha()
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        
        # Set up finish line
        self.finish_line = pygame.image.load(FINISHLINE).convert_alpha()
        finishline_width, finishline_height = level_data["finishline_size"]
        self.finish_line = pygame.transform.scale(self.finish_line, (finishline_width, finishline_height))
        self.finish_line_position = level_data["finishline_pos"]
        self.finish_mask = pygame.mask.from_surface(self.finish_line)
        
        # Reset car position
        start_x, start_y = level_data["car_start_pos"]
        self.car.reset(start_x, start_y)
        
        # Initialize timer for the level
        self.remaining_time = level_data["target_time"]
        self.game_state = "running"

        
    def draw(self):
        self.ground_group.draw(self.surface)
        
        # Draw track and elements
        self.surface.blit(self.track, (0, 0))
        self.surface.blit(self.track_border, (0, 0))
        self.surface.blit(self.finish_line, self.finish_line_position)
        
        # Draw car and rays
        blit_rotate_center(self.surface, self.car.image, 
                          (self.car.x, self.car.y), self.car.angle)

    def draw_ui(self):        
        # Timer - now showing remaining time
        timer_color = RED if self.remaining_time < 3 else GREEN
        timer_text = font_scale(27).render(
            f"Time Remaining: {self.remaining_time:.1f}", 
            True, timer_color)
        self.surface.blit(timer_text, (10, 5))

    def draw_level_complete(self):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 128))
        self.surface.blit(surface, (0, 0))
        
        if self.remaining_time > 0:
            text = font_scale(60).render("Level Complete!", True, GREEN)
            time_text = font_scale(40).render(
                f"Time Remaining: {self.remaining_time:.1f}", True, WHITE)
            next_text = font_scale(30).render("Press SPACE to continue", True, WHITE)
        else:
            text = font_scale(60).render("Time's Up!", True, RED)
            time_text = font_scale(40).render(
                "Try to complete the track faster!", True, WHITE)
            next_text = font_scale(30).render("Press SPACE to retry", True, WHITE)
        
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        next_rect = next_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        
        self.surface.blit(text, text_rect)
        self.surface.blit(time_text, time_rect)
        self.surface.blit(next_text, next_rect)

    def draw_game_complete(self):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 180))
        self.surface.blit(surface, (0, 0))
        
        text = font_scale(80).render("Congratulations!", True, GOLD)
        complete_text = font_scale(40).render("You've completed all levels!", True, WHITE)
        restart_text = font_scale(30).render("Press SPACE to play again", True, WHITE)
        
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        complete_rect = complete_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        
        self.surface.blit(text, text_rect)
        self.surface.blit(complete_text, complete_rect)
        self.surface.blit(restart_text, restart_rect)

    def draw_countdown(self, count):
        #level
        Level_Text = font_scale(100).render(self.current_level_data["Level"], True, GREEN)
        Level_Rect = Level_Text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        self.surface.blit(Level_Text, Level_Rect)

        # Shadow effect
        shadow = font_scale(175, COUNTDOWN_FONT).render(str(count), True, BLACK)
        shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surface.blit(shadow, (0, 0))
        shadow_surface.set_alpha(200)
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 2 + 5))
        
        # Main countdown number
        text = font_scale(175, COUNTDOWN_FONT).render(str(count), True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        self.surface.blit(shadow_surface, shadow_rect)
        self.surface.blit(text, text_rect)

    def handle_completion(self):
        if self.remaining_time > 0:
            if self.current_level < len(LEVELS) - 1:
                self.current_level += 1
                self.remaining_time = 0
                self.load_level(self.current_level)
            else:
                self.game_state = "game_complete"
        else:
            self.load_level(self.current_level)  # Retry level

    def restart_game(self):
        self.load_level(self.current_level)
        self.game_state = "running"

    def update(self):
        if self.game_state == "running":
            # Update timer
            if self.remaining_time > 0:
                self.remaining_time -= 1/FPS  # Decrease by the frame time
                if self.remaining_time <= 0:
                    self.game_state = "level_complete"
                    self.handle_music(False)
                    return
            
            # Check for level completion
            if self.move():  # Level complete
                self.game_state = "level_complete"
                self.handle_music(False)

    def move(self):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.car.accelerate(True)
            moving = True
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.car.accelerate(False)
            moving = True

        if keys[pygame.K_a]:
            self.car.rotate(left=True)
        if keys[pygame.K_d]:
            self.car.rotate(right=True)

        if not moving:
            self.car.reduce_speed()

        collision = self.check_collision()
        finish = self.check_finish()
        
        return finish

    def check_collision(self):
        collision = self.car.collide(self.track_border_mask)
        if collision:
            self.car.handle_border_collision()
            self.collide_sound.play()
        return collision

    def check_finish(self):
        finish_pos = self.car.collide(self.finish_mask, *self.finish_line_position)
        if finish_pos:
            if finish_pos[1] == 0:
                self.car.handle_border_collision()
            else:
                self.win_sound.play()
                return True
        return False

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