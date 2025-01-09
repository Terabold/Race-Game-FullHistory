import torch
import numpy as np
import pygame
from Constants import *
from Car import Car
from Checkpoint import Checkpoint

def font_scale(size, Font=FONT):
    return pygame.font.Font(Font, size)

def blit_rotate_center(game, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    game.blit(rotated_image, new_rect.topleft)

class Environment:
    def __init__(self, surface, sound_enabled=True, auto_respawn=False, car_color="Red") -> None:
        self.surface = surface
        self.grass = pygame.image.load(GRASS).convert()
        self.cached_grass = pygame.transform.scale(self.grass, (WIDTH, HEIGHT))
        self.current_level = 0
        self.auto_respawn = auto_respawn
        self.sound_enabled = sound_enabled
        
        self.paused = False
        start_pos = LEVELS[0]["car_start_pos"]
        self.car = Car(start_pos[0], start_pos[1], car_color)
        self.car_group = pygame.sprite.GroupSingle(self.car)
        
        # Initialize checkpoint group
        self.checkpoint_group = pygame.sprite.Group()
        self.current_checkpoint_index = 0
        
        self.load_level(self.current_level)
        self.setup_sound()
        self.remaining_time = LEVELS[0]["target_time"]
        self.game_state = "countdown"
        self.previous_state = None
        
    def load_level(self, level_index):
        level_data = LEVELS[level_index]
        self.current_level_data = level_data
        
        # Basic level loading
        self.track = pygame.image.load(level_data["track_image"]).convert_alpha()
        self.track_border = pygame.image.load(level_data["border_image"]).convert_alpha()
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        
        self.finish_line = pygame.image.load(FINISHLINE).convert_alpha()
        finishline_width, finishline_height = level_data["finishline_size"]
        self.finish_line = pygame.transform.scale(self.finish_line, (finishline_width, finishline_height))
        self.finish_line_position = level_data["finishline_pos"]
        self.finish_mask = pygame.mask.from_surface(self.finish_line)
        
        # Reset car position
        start_x, start_y = level_data["car_start_pos"]
        self.car.reset(start_x, start_y)
        
        # Reset game state
        self.remaining_time = level_data["target_time"]
        self.game_state = "countdown"
        
        # Clear existing checkpoints
        self.checkpoint_group.empty()
        self.current_checkpoint_index = 0
        
        # Load checkpoints
        if "checkpoints" in level_data:
            for i, checkpoint_data in enumerate(level_data["checkpoints"]):
                checkpoint = Checkpoint(
                    checkpoint_data["pos"],
                    checkpoint_data["size"],
                    i
                )
                self.checkpoint_group.add(checkpoint)

    def get_closest_active_checkpoint(self):
        """Get the next unpassed checkpoint closest to the car"""
        active_checkpoints = [cp for cp in self.checkpoint_group.sprites() 
                            if not cp.passed and cp.index >= self.current_checkpoint_index]
        if not active_checkpoints:
            return None
            
        # Sort checkpoints by both index and distance
        active_checkpoints.sort(key=lambda cp: (
            cp.index != self.current_checkpoint_index,  # Prioritize current index
            cp.get_distance_to(self.car.x, self.car.y)  # Then by distance
        ))
        
        return active_checkpoints[0] if active_checkpoints else None
    
    def check_checkpoints(self):
        closest_checkpoint = self.get_closest_active_checkpoint()
        if not closest_checkpoint:
            return
            
        if self.car.collide(closest_checkpoint.mask, *closest_checkpoint.pos):
            closest_checkpoint.passed = True
            self.current_checkpoint_index = closest_checkpoint.index + 1
            self.checkpoint_sound.play()

    def run_countdown(self):
        if self.game_state == "countdown":
            self.countdown_sound.play()
            for i in range(3, 0, -1):
                self.draw()
                self.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)
            self.handle_music(True)
            self.game_state = "running"

    def draw(self):
        # Draw base game elements
        self.surface.blits((
            (self.cached_grass, (0, 0)),
            (self.track, (0, 0)),
            (self.finish_line, self.finish_line_position),
        ))

        # Only draw the closest active checkpoint
        closest_checkpoint = self.get_closest_active_checkpoint()
        if closest_checkpoint:
            self.surface.blit(closest_checkpoint.image, closest_checkpoint.rect)
        
        # Draw track border after checkpoints
        self.surface.blit(self.track_border, (0, 0))
        
        # Draw car
        blit_rotate_center(self.surface, self.car.image, 
                          (self.car.x, self.car.y), self.car.angle)
        
        # Draw UI overlays
        if self.game_state == "paused":
            self.draw_pause_overlay()
        elif self.game_state == "running":
            self.draw_ui()
        elif self.game_state == "level_complete":
            self.draw_level_complete()
        elif self.game_state == "game_complete":
            self.draw_game_complete()

    def draw_pause_overlay(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.surface.blit(overlay, (0, 0))
        
        # Draw pause text
        paused_text = font_scale(75).render("GAME PAUSED", True, GREEN)
        resume_text = font_scale(30).render("Press ESC to Resume", True, WHITE)
        time_text = font_scale(30).render(
            f"Time Remaining: {self.remaining_time:.1f}", True, WHITE)
        
        paused_rect = paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        
        self.surface.blit(paused_text, paused_rect)
        self.surface.blit(resume_text, resume_rect)
        self.surface.blit(time_text, time_rect)

    def draw_ui(self):  
        #timer      
        timer_color = RED if self.remaining_time < 1 else GREEN
        timer_text = font_scale(27).render(
            f"Time Remaining: {self.remaining_time:.1f}", 
            True, timer_color)
        self.surface.blit(timer_text, (10, 5))

    def toggle_pause(self):
        if self.game_state == "paused":
            self.game_state = self.previous_state
            if self.game_state == "running":
                self.handle_music(True)
        elif self.game_state in ["running", "countdown"]:
            self.previous_state = self.game_state
            self.game_state = "paused"
            self.handle_music(False)

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
        surface.fill((0, 0, 0, 200))
        self.surface.blit(surface, (0, 0))
        
        text = font_scale(80).render("Congratulations!", True, GOLD)
        complete_text1 = font_scale(40).render(f"You've completed all levels", True, WHITE)
        complete_text2= font_scale(40).render(f"You beat this level with {self.remaining_time:.1f} seconds remaining!", True, WHITE)
        restart_text = font_scale(30).render("Press SPACE to play all levels again", True, WHITE)
        
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        complete1_rect = complete_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        complete2_rect = complete_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))
        
        self.surface.blit(text, text_rect)
        self.surface.blit(complete_text1, complete1_rect)
        self.surface.blit(complete_text2, complete2_rect)
        self.surface.blit(restart_text, restart_rect)

    def draw_countdown(self, count):
        Level_Text = font_scale(100).render(self.current_level_data["Level"], True, GOLD)
        Level_Rect = Level_Text.get_rect(center=(WIDTH // 2, 75))
        self.surface.blit(Level_Text, Level_Rect)

        shadow = font_scale(175, COUNTDOWN_FONT).render(str(count), True, BLACK)
        shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surface.blit(shadow, (0, 0))
        shadow_surface.set_alpha(200)
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 2 + 5))
        
        text = font_scale(175, COUNTDOWN_FONT).render(str(count), True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        self.surface.blit(shadow_surface, shadow_rect)
        self.surface.blit(text, text_rect)

    def handle_completion(self):
        if self.remaining_time > 0:
            if self.current_level < len(LEVELS) - 1:
                self.game_state = "level_complete"
                self.current_level += 1
                self.load_level(self.current_level)
            else:
                self.game_state = "game_complete"
                self.handle_music(False)
        else:
            self.load_level(self.current_level)

    def restart_game(self):
        self.current_level = 0
        self.handle_music(False)
        self.load_level(self.current_level)
        
    def restart_level(self):
        self.handle_music(False)
        self.load_level(self.current_level)

    def update(self):
        if self.game_state == "countdown":
            self.run_countdown()
        elif self.game_state == "running":
            if self.remaining_time > 0:
                self.remaining_time -= 1/FPS
                if self.remaining_time <= 0:
                    if self.auto_respawn:
                        self.restart_level()
                        self.remaining_time = self.current_level_data["target_time"]
                        self.game_state = "countdown"
                    else:
                        self.game_state = "level_complete"
                        self.handle_music(False)
            self.check_collision()
            self.check_checkpoints()

    def move(self, action):
        if self.game_state != "running":
            return False

        moving = False
        if action == 1 or action in [5, 6]:
            self.car.accelerate(True)
            moving = True
        elif action == 2 or action in [7, 8]:
            self.car.accelerate(False)
            moving = True
        
        if action in [3, 5, 7]:
            self.car.rotate(left=True)
        elif action in [4, 6, 8]:
            self.car.rotate(right=True)

        if not moving:
            self.car.reduce_speed()

        self.check_collision()
        return self.check_finish()

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
                # Check if all checkpoints in the checkpoint group have been passed
                if all(cp.passed for cp in self.checkpoint_group.sprites()):
                    self.win_sound.play()
                    self.handle_music(False)
                    if self.current_level < len(LEVELS) - 1:
                        self.game_state = "level_complete"
                    else:
                        self.game_state = "game_complete"
                    return True
                else:
                    self.car.handle_border_collision()
        return False

    def setup_sound(self):
        volume_multiplier = 1 if self.sound_enabled else 0
        
        self.background_music = pygame.mixer.Sound(BACKGROUND_MUSIC)
        self.background_music.set_volume(0.01 * volume_multiplier)
        
        self.countdown_sound = pygame.mixer.Sound(COUNTDOWN_SOUND)
        self.countdown_sound.set_volume(0.1 * volume_multiplier)
        
        self.collide_sound = pygame.mixer.Sound(COLLIDE_SOUND)
        self.collide_sound.set_volume(4 * volume_multiplier)
        
        self.win_sound = pygame.mixer.Sound(WIN_SOUND)
        self.win_sound.set_volume(0.2 * volume_multiplier)
        
        self.checkpoint_sound = pygame.mixer.Sound(CHECKPOINT_SOUND)
        self.checkpoint_sound.set_volume(0.3 * volume_multiplier)
        
        self.is_music_playing = False

    def handle_music(self, play=True):
        if play and not self.is_music_playing:
            self.background_music.play(-1)
            self.is_music_playing = True
        elif not play:
            self.background_music.stop()
            self.is_music_playing = False

    def state(self):
        # Car state values
        car_pos = 2                    # x, y = 2
        car_velocity = 1               # velocity = 1
        car_angle = 1                  # angle = 1
        car_drift = 2                  # drift_momentum, drift_friction = 2
        
        # Track/game values
        finish_line = 4                # x, y, width, height = 4
        border_collisions = 3          # recovery_bounce, recovery_slowdown, recovery_straighten = 3
        game_state = 4                 # remaining_time, current_level, max_velocity, acceleration = 4
        
        total = car_pos + car_velocity + car_angle + car_drift + finish_line + border_collisions + game_state
        # total = 17
        
        state_list = []
        
        # Car position and movement (0-5)
        state_list.extend([
            self.car.x / WIDTH,                    # Normalize positions
            self.car.y / HEIGHT,
            self.car.velocity / self.car.max_velocity,
            self.car.angle / 360.0,
            self.car.drift_momentum / self.car.max_velocity,
            self.car.drift_friction
        ])
        
        # Finish line info (6-9)
        state_list.extend([
            self.finish_line_position[0] / WIDTH,
            self.finish_line_position[1] / HEIGHT,
            self.current_level_data["finishline_size"][0] / WIDTH,
            self.current_level_data["finishline_size"][1] / HEIGHT
        ])
        
        # Collision physics (10-12)
        state_list.extend([
            self.car.recovery_bounce,
            self.car.recovery_slowdown,
            self.car.recovery_straighten
        ])
        
        # Game state (13-16)
        state_list.extend([
            self.remaining_time / self.current_level_data["target_time"],
            self.current_level / len(LEVELS),
            self.car.max_velocity / MAXSPEED,
            self.car.acceleration / ACCELERATION
        ])
        
        return torch.tensor(state_list, dtype=torch.float32)