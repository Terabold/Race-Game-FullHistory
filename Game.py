import pygame
import sys
import time
from Environment import Environment
from save_time import TimeManager
from Constants import *

def init_game():
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")
    clock = pygame.time.Clock()
    environment = Environment(surface)
    save_time = TimeManager()
    return surface, clock, environment, save_time

def handle_countdown(surface, environment):
    environment.restart()
    environment.countdown_sound.play()
    
    for i in range(3, 0, -1):
        surface.fill((0, 0, 0))
        environment.draw()
        environment.draw_countdown(i)
        pygame.display.update()
        pygame.time.wait(1000)
    
    
    environment.start_time = time.time()
    environment.start_music()
    return True

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return True, True
    return True, False

def main():
    surface, clock, environment, save_time = init_game()
    
    run = True
    car_can_move = False
    countdown_done = False
    reset_requested = False
    game_over = False

    while run:
        clock.tick(FPS)

        # Handle events
        run, reset_requested = handle_events()
        if reset_requested:
            countdown_done = False
            game_over = False
            environment.stop_music()

        # Handle countdown
        if not countdown_done and not game_over:
            countdown_done = handle_countdown(surface, environment)
            car_can_move = True
            reset_requested = False

        # Game state updates
        if car_can_move and not game_over:
            done = environment.move()
        
            if environment.start_time:
                elapsed_time = time.time() - environment.start_time
                environment.update_time(elapsed_time)

            if done:
                game_over = True
                car_can_move = False
                environment.stop_music()
                save_time.save_time(environment.elapsed_time)

        # Update and draw
        environment.update()
        environment.draw()
        
        if game_over:
            environment.draw_winner()
        else:
            environment.draw_ui(clock)

        pygame.display.update()

        # Handle restart after game over
        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_over = False
                countdown_done = False
                car_can_move = False
                environment.restart()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()