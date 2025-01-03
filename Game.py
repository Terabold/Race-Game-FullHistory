import pygame
import sys
from Environment import Environment
from Human_Agent import Human_Agent
from Constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")
    clock = pygame.time.Clock()
    environment = Environment(surface)
    player = Human_Agent()

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    environment.restart_level()
                elif event.key == pygame.K_SPACE:
                    if environment.game_state == "level_complete":
                        environment.handle_completion()
                    elif environment.game_state == "game_complete":
                        environment.restart_game()
        
        environment.update()
        if environment.game_state == "running":
            environment.move(player.get_action())
        
        environment.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()
