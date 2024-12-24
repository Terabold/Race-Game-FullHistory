from utils import scale_img, scale_finishline, blit_rotate_center, font_scale
import pygame


def load_assets():
        assets = {
            "car": scale_img(pygame.image.load(r'photo\car.png').convert_alpha(), 0.5),
            "track_border": pygame.image.load(r'photo\track-stretch-border-2.png').convert_alpha(),
            "background": pygame.image.load(r'photo\background_menu.jpeg').convert(),
            "grass": pygame.image.load(r'photo\grass2.jpg').convert(),
            "track": pygame.image.load(r'photo\track-stretch.png').convert_alpha(),
            "finish_line": scale_finishline(pygame.image.load(r'photo\finish.png').convert(), 2),
            'win_sound' : pygame.mixer.Sound(r'sound\mixkit-completion-of-a-level-2063.wav'),
            'coundown' : pygame.mixer.Sound(r'sound\game-countdown-62-199828.mp3'),
        }
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

    @staticmethod
    def scale_image(img, factor):
        return scale_img(img, factor)
    
    @staticmethod
    def scale_finish_line(img, factor):
        return scale_finishline(img, factor)