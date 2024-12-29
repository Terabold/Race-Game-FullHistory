import pygame
from Car import Car
from Ground import Ground
from Constants import *

def font_scale(size):
    return pygame.font.Font(r'fonts\PressStart2P-Regular.ttf', size)

def blit_rotate_center(game, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(topleft = top_left).center)
    game.blit(rotated_image, new_rect.topleft)

class Environment:
    def __init__(self, surface) -> None:
        # Initialize the game surface
        self.surface = surface
        
        # Create ground (track) and its sprite group
        self.ground = Ground()
        self.ground_group = pygame.sprite.GroupSingle(self.ground)
        
        # Load track border
        self.track_border = pygame.image.load(TRACKBORDER).convert_alpha()
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        
        # Load finish line
        self.finish_line = pygame.image.load(FINISHLINE).convert_alpha()
        self.finish_line = pygame.transform.scale(self.finish_line, (150,25))
        self.finish_line_position = FINISHLINE_POSITION
        self.finish_mask = pygame.mask.from_surface(self.finish_line)
        
        #Load music
        self.background_music = pygame.mixer.Sound(BACKGROUND_MUSIC)
        self.background_music.set_volume(0.01)
        self.is_music_playing = False  # Track if music is playing

        #load countdown sound
        self.countdown_sound = pygame.mixer.Sound(COUNTDOWN_SOUND)
        self.countdown_sound.set_volume(0.1)

        #load collide sound
        self.collide_sound = pygame.mixer.Sound(COLLIDE_SOUND)
        self.collide_sound.set_volume(4)

        #load win sound
        self.win_sound = pygame.mixer.Sound(WIN_SOUND)
        self.win_sound.set_volume(0.2)
        
        # Create car and its sprite group
        self.car = Car()
        self.car_group = pygame.sprite.GroupSingle(self.car)
        
        # Game state variables
        self.lap_count = 0
        self.elapsed_time = 0
        self.start_time = None
        self.winner = 0


    def stop_music(self):
        self.background_music.stop()
        self.is_music_playing = False
        return False

    def start_music(self):
        if not self.is_music_playing:
            self.background_music.play(-1)  # Loop indefinitely
            self.is_music_playing = True
        return True

    def update_time(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def update(self):
        self.car_group.update()
    
    def draw(self):
        # Draw background
        self.ground_group.draw(self.surface)

        # Draw track border and finish line
        self.surface.blit(self.track_border, (0, 0))
        self.surface.blit(self.finish_line, self.finish_line_position)

        # Draw rotated car
        blit_rotate_center(self.surface, self.car.image, (self.car.x, self.car.y), self.car.angle)

    def draw_ui(self, clock):
        # FPS
        fps_text = font_scale(18).render(f"FPS: {int(clock.get_fps())}", True, WHITE)
        self.surface.blit(fps_text, (10, 10))

        if self.elapsed_time > 0:
            # Time
            timer_text = font_scale(25).render(f"Time: {self.elapsed_time:.2f}", True, WHITE)
            timer_height = timer_text.get_height()
            self.surface.blit(timer_text, (10, self.surface.get_height() - 40))

            # Velocity
            vel_text = font_scale(25).render(f"Vel: {round(self.car.velocity * 10, 1):.0f}m/s", True, WHITE)
            self.surface.blit(vel_text, (10, self.surface.get_height() - 45 - timer_height))

    def draw_countdown(self, count):
        # Render foggy shadow (slightly offset)
        shadow = font_scale(100).render(str(count), True, FOGGRAY)  # Fog-like gray shadow
        shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surface.blit(shadow, (0, 0))
        shadow_surface.set_alpha(150)  # Make the shadow semi-transparent
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 2 + 5))
        
        # Render the main text
        text_color = (220, 20, 60)  # Crimson red color
        text = font_scale(100).render(str(count), True, text_color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Draw the shadow and the main text
        self.surface.blit(shadow_surface, shadow_rect)
        self.surface.blit(text, text_rect)

    def draw_winner(self):   
        winner_text =  f"Time: {self.elapsed_time:.2f} sec" 
        winner_text = font_scale(40).render(winner_text, True, GOLD)
        restart_text = font_scale(40).render("Press SPACE to play again", True, GREEN)
        
        winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        
        self.surface.blit(winner_text, winner_rect)
        self.surface.blit(restart_text, restart_rect)

    def restart(self, new_game=True):
        if new_game:
            self.lap_count = 0
            self.elapsed_time = 0
            
        self.car.reset()
        self.game_started = False

    def check_collision(self):
        return self.car.collide(self.track_border_mask)

    def check_finish_line(self):
        return self.car.collide(self.finish_mask, *self.finish_line_position)

    def move(self, action):
        reward = 0
        done = False
        # Get the state of all keys
        keys = pygame.key.get_pressed()

        if action == 1 or keys[pygame.K_w]: 
            self.car.move_forward()

        if action == 2 or keys[pygame.K_s]: 
            self.car.move_backward()

        if action == 3 or keys[pygame.K_a]: 
            self.car.rotate(left=True)

        if action == 4 or keys[pygame.K_d]:  
            self.car.rotate(right=True)

        if action == 0 or (not keys[pygame.K_w] and not keys[pygame.K_s]): 
            self.car.reduce_speed()

        if self.check_collision():
            self.car.handle_border_collision()
            self.collide_sound.play()
            reward -= 1  

        finish_touch = self.check_finish_line()
        if finish_touch:
            if finish_touch[1] == 0:  
                self.car.handle_finishline_collision()
                reward -= 2 
            else:
                self.win_sound.play()
                reward += 5  
                self.lap_count += 1
                # if self.lap_count >= LAPS:
                #     reward += 5  
                done = True

        return reward, done

    def state(self):
        """Return current state for AI"""
        # This will need to be expanded based on what state information
        # you want to feed to your AI
        state_list = [
            self.car.x,              # Car X position
            self.car.y,              # Car Y position
            self.car.angle,          # Car angle
            self.car.velocity,       # Car velocity
            self.lap_count,          # Current lap
            self.elapsed_time,       # Time elapsed
            self.car.collide()       # Is Colliding
        ]
        return state_list