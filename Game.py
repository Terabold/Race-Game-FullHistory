import pygame
import sys
import time
from Environment import Environment
from save_time import TimeManager
from Human_Agent import Human_Agent
from Constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    
    # Initialize window and graphics
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")
    clock = pygame.time.Clock()

    environment = Environment(surface)
    player = Human_Agent()

    run = True
    car_can_move = False
    countdown_done = False
    reset_requested = False
    game_over = False
    save_time = TimeManager()

    while run:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_requested = True
                    environment.stop_music()
                    countdown_done = False
                    game_over = False

        # Handle game reset
        if reset_requested:
            reset_requested = False
            countdown_done = False
            game_over = False
            environment.stop_music()

        # Handle countdown
        if not countdown_done and not game_over:
            environment.restart()
            environment.countdown_sound.play()
            for i in range(3, 0, -1):
                surface.fill((0, 0, 0))  # Clear screen
                environment.draw()
                environment.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)
            
            countdown_done = True
            car_can_move = True
            reset_requested = False
            environment.start_time = time.time()
            environment.start_music()

        # Game state updates
        if car_can_move and not game_over:
            action = player.get_Action(pygame.key.get_pressed())
            reward, done = environment.move(action=action)
        
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