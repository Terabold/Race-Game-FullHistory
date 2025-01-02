import pygame
import sys
import time
from Environment import Environment
from Constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")
    clock = pygame.time.Clock()
    environment = Environment(surface)
    
    game_active = False
    countdown_active = False

    while True:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle restart with R key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    environment.restart_game()
                    game_active = False
                    countdown_active = False
                    environment.handle_music(False)
                
                # Space to continue/retry level or restart game
                elif event.key == pygame.K_SPACE:
                    if environment.game_state == "level_complete":
                        environment.handle_completion()
                        if environment.game_state != "game_complete":
                            game_active = False
                            countdown_active = False
                    elif environment.game_state == "game_complete":
                        environment.restart_game()
                        game_active = False
                        countdown_active = False

        # Handle countdown sequence
        if not game_active and not countdown_active and environment.game_state == "running":
            countdown_active = True
            environment.countdown_sound.play()
            for i in range(3, 0, -1):
                surface.fill(environment.current_level_data["background_color"])
                environment.draw()
                environment.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)
            
            environment.handle_music(True)
            game_active = True
            countdown_active = False

        # Game state updates
        if game_active and environment.game_state == "running":
            environment.update()
        
        # Rendering
        surface.fill(environment.current_level_data["background_color"])
        environment.draw()
        
        # Draw appropriate overlay based on game state
        if environment.game_state == "running":
            environment.draw_ui()
        elif environment.game_state == "level_complete":
            environment.draw_level_complete()
        elif environment.game_state == "game_complete":
            environment.current_level = 0
            environment.draw_game_complete()
        
        pygame.display.update()

if __name__ == "__main__":
    main()