from utils import blit_rotate_center, font_scale
import pygame

def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def scale_finishline(img, factor):
    size = round(img.get_width() * factor), round(img.get_height())
    return pygame.transform.scale(img, size)

def load_assets():
        assets = {
            "car": scale_img(pygame.image.load(r'photo\car.png').convert_alpha(), 0.5),
            "track_border": pygame.image.load(r'photo\track-stretch-border-2.png').convert_alpha(),
            "background": pygame.image.load(r'photo\background_menu.jpeg').convert(),
            "grass": pygame.image.load(r'photo\grass2.jpg').convert(),
            "track": pygame.image.load(r'photo\track-stretch.png').convert_alpha(),
            "finish_line": scale_finishline(pygame.image.load(r'photo\finish.png').convert(), 2),
            'win_sound' : pygame.mixer.Sound(r'sound\mixkit-completion-of-a-level-2063.wav'),
            'countdown' : pygame.mixer.Sound(r'sound\game-countdown-62-199828.mp3'),
            'background_music': pygame.mixer.Sound(r'sound\y2mate.com - KSI  Thick Of It ft Trippie Redd.mp3'),
            'cheater_sound': pygame.mixer.Sound(r'sound\y2mate.com - Among us sus sound effect.mp3')  # Add your music file
        }
        assets['win_sound'].set_volume(0.3)
        assets['cheater_sound'].set_volume(0.3)
        assets['countdown'].set_volume(0.2)
        assets['background_music'].set_volume(0.1)
        finish_line_position = [250, 250] 
        return assets, finish_line_position

class Graphic:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_display = pygame.display.set_mode((width, height))

    def draw_no_ui(self, state, images):
        self._draw_environment(images)
        self._draw_car(state.car)
        pygame.display.update()

    def draw(self, state, images, clock):
        """Main drawing function"""
        self._draw_environment(images)
        self._draw_car(state.car)
        self._draw_ui(state, clock)
        pygame.display.update()
        
    def _draw_environment(self, images):
        for img, pos in images:
            self.game_display.blit(img, pos)
            
    def _draw_car(self, car):
        blit_rotate_center(self.game_display, car.img, (car.x, car.y), car.angle)
        
    def _draw_ui(self, state, clock):
        # FPS
        fps_text = font_scale(18).render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        self.game_display.blit(fps_text, (10, 10))
        
        #vel and time
        if state.elapsed_time > 0:
            timer_text = font_scale(25).render(f"Time: {state.elapsed_time:.2f}", True, (255, 255, 255))
            timer_height = timer_text.get_height()
            self.game_display.blit(timer_text, (10, self.height - 40))
            # Velocity
            vel_text = font_scale(25).render(f"Vel: {round(state.car.vel*10, 1):.0f}m/s", 1, (255, 255, 255))
            self.game_display.blit(vel_text, (10, self.game_display.get_height() - 45 - timer_height))


    def draw_countdown(self, count):
        # Render foggy shadow (slightly offset)
        shadow = font_scale(100).render(str(count), True, (50, 50, 50))  # Fog-like gray shadow
        shadow_surface = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
        shadow_surface.blit(shadow, (0, 0))
        shadow_surface.set_alpha(150)  # Make the shadow semi-transparent
        shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 5, self.height // 2 + 5))
        
        # Render the main text
        text_color = (220, 20, 60)  # Crimson red color
        text = font_scale(100).render(str(count), True, text_color)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        
        # Draw the shadow and the main text
        self.game_display.blit(shadow_surface, shadow_rect)
        self.game_display.blit(text, text_rect)
    
    def draw_winner(self, state):       
        winner_text = font_scale(40).render(state.winner, True, (255, 215, 0))
        restart_text = font_scale(40).render("Press SPACE to play again", True, (0, 255, 0))
        
        winner_rect = winner_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        
        self.game_display.blit(winner_text, winner_rect)
        self.game_display.blit(restart_text, restart_rect)

    def cheater(self):
        # Create Warning text with shadow
        warning_text = font_scale(40).render("We Caught You Cheating", True, (255, 0, 0))
        warning_shadow = font_scale(40).render("We Caught You Cheating", True, (50, 50, 50))
        
        # Create restart text with shadow
        restart_text = font_scale(40).render("Press SPACE to play again fairly", True, (255, 0, 0))
        restart_shadow = font_scale(40).render("Press SPACE to play again fairly", True, (50, 50, 50))
        
        # Create shadow surfaces with transparency
        warning_shadow_surface = pygame.Surface(warning_shadow.get_size(), pygame.SRCALPHA)
        warning_shadow_surface.blit(warning_shadow, (0, 0))
        
        restart_shadow_surface = pygame.Surface(restart_shadow.get_size(), pygame.SRCALPHA)
        restart_shadow_surface.blit(restart_shadow, (0, 0))
        
        # Get rectangles for positioning
        warning_rect = warning_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        warning_shadow_rect = warning_shadow_surface.get_rect(
            center=(self.width // 2 + 5, self.height // 2 - 45)  # Offset shadow slightly
        )
        
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        restart_shadow_rect = restart_shadow_surface.get_rect(
            center=(self.width // 2 + 5, self.height // 2 + 55)  # Offset shadow slightly
        )
        
        # Draw shadows first, then main text
        self.game_display.blit(warning_shadow_surface, warning_shadow_rect)
        self.game_display.blit(restart_shadow_surface, restart_shadow_rect)
        self.game_display.blit(warning_text, warning_rect)
        self.game_display.blit(restart_text, restart_rect)

