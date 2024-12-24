import pygame
import time
from graphic import Graphic
from graphic import load_assets
from Agent import Car
from Environment import Environment
from State import State
from action import Action


def main():
    pygame.init()
    pygame.mixer.init()
    
    # Initialize window and graphics
    width, height = 1600, 900 
    graphics = Graphic(width, height)
    pygame.display.set_caption("Racing Game")
    
    # Load and scale images
    assets, finish_line_position = load_assets()

    #intilize car
    car = Car(5, 5)  
    car.set_image(assets["car"]) 

    #intilize state
    state = State(car)

    #intilize environment
    environment = Environment(assets["track"], assets["track_border"], assets["finish_line"], finish_line_position)
    images = environment.setup_images(assets["grass"], assets["track"])

    
    state = State(car)
    action = Action(car)    
    
    # Game loop variables
    clock = pygame.time.Clock()
    run = True
    car_moving = False
    countdown_done = False
    reset_requested = False

    while run:
        clock.tick(60)
        
        # Handle events
        run = action.handle_events(run)

        if action.reset_requested:
            action.reset_requested = False  # Clear the flag
            countdown_done = False

        # Handle countdown and reset
        if reset_requested or not countdown_done:
            action.reset()
            assets['coundown'].play()
            for i in range(3, 0, -1):
                graphics.draw_no_ui(state, images)
                graphics.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)     
            countdown_done = True
            car_moving = True
            reset_requested = False
            environment.start_time = time.time()

        # Update game state
        if car_moving:
            # Handle input
            action.handle_input(pygame.key.get_pressed())

            # Update elapsed time
            if environment.start_time:
                elapsed_time = time.time() - environment.start_time
                state.update(elapsed_time)

            # Check collisions
            if environment.check_collision(car):
                car.bounce()

            # Check finish
            finish_touch = environment.check_finish(car)
            if finish_touch:
                if finish_touch[1] == 0:
                    car.bounceextra()
                else:
                    car_moving = False
                    state.set_winner(elapsed_time)
                    assets['win_sound'].set_volume(0.5)
                    assets['win_sound'].play()
                    # Draw winner and restart text
                    graphics.draw_winner(state)
                    pygame.display.update()
                    
                    # Wait for space key
                    waiting_for_restart = True
                    while waiting_for_restart:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                waiting_for_restart = False
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    # Reset everything for a new game
                                    state.reset()
                                    action.reset()
                                    environment.start_time = None
                                    countdown_done = False
                                    car_moving = False
                                    waiting_for_restart = False
                    
        # Draw current game state
        graphics.draw(state, images, clock)

    pygame.quit()

if __name__ == "__main__":
    main()