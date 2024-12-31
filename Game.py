import pygame
import sys
import time
from Environment import Environment
from save_time import TimeManager
from Constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")
    clock = pygame.time.Clock()
    environment = Environment(surface)
    save_time = TimeManager()
    
    running = True
    car_moving = False
    countdown_complete = False
    game_over = False

    while running:
        clock.tick(FPS)

        # Handle quit and reset
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                countdown_complete = False
                game_over = False
                environment.handle_music(False)

        # Handle countdown
        if not countdown_complete and not game_over:
            environment.restart()
            environment.countdown_sound.play()
            
            for i in range(3, 0, -1):
                surface.fill((0, 0, 0))
                environment.draw()
                environment.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)
            
            environment.start_time = time.time()
            environment.handle_music(True)
            countdown_complete = True
            car_moving = True

        # Game updates
        if car_moving and not game_over:
            if environment.move():
                game_over = True
                car_moving = False
                environment.handle_music(False)
                save_time.save_time(environment.elapsed_time)
            
            if environment.start_time:
                environment.update_time(time.time() - environment.start_time)

        # Rendering
        environment.draw()
        if game_over:
            environment.draw_winner()
        else:
            environment.draw_ui()
        pygame.display.update()

        # Handle restart
        if game_over and pygame.key.get_pressed()[pygame.K_SPACE]:
            game_over = False
            countdown_complete = False
            car_moving = False
            environment.restart()

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()