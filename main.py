import pygame
import time
from graphic import Graphic, load_assets
from Agent import Car
from Environment import Environment
from State import State
from action import Action
from save_time import TimeManager

def main():
    pygame.init()
    pygame.mixer.init()
    
    # Initialize window and graphics
    graphics = Graphic()
    pygame.display.set_caption("Racing Game")
    
    # Load and scale images
    assets, finish_line_position = load_assets()

    #initialize car
    car = Car(5, 5)  
    car.set_image(assets["car"]) 

    #initialize environment
    environment = Environment(assets["track"], assets["track_border"], assets["finish_line"], finish_line_position)
    images = environment.setup_images(assets["grass"], assets["track"])
    
    state = State(car)
    action = Action(car)    
    
    # Game loop variables
    run = True
    car_moving = False
    countdown_done = False
    reset_requested = False
    save_time = TimeManager()


    def stop_music():
        assets['background_music'].stop()
        return False

    def start_music():
        assets['background_music'].play(-1)  # -1 means loop indefinitely
        return True
    
    while run:
        graphics.clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    action.reset_requested = True
                    stop_music()
                    countdown_done = False

        if action.reset_requested:
            action.reset_requested = False
            countdown_done = False
            stop_music()

        # Handle countdown and reset
        if reset_requested or not countdown_done:
            action.reset()
            assets['countdown'].play()
            for i in range(3, 0, -1):
                graphics.draw_no_ui(state, images)
                graphics.draw_countdown(i)
                pygame.display.update()
                pygame.time.wait(1000)
            
            countdown_done = True
            car_moving = True
            reset_requested = False
            environment.start_time = time.time()
            
            # Start music 1 second after countdown
            start_music()

        # Update game state
        if car_moving:
            action.handle_input(pygame.key.get_pressed())

            if environment.start_time:
                elapsed_time = time.time() - environment.start_time
                state.update(elapsed_time)

            # Check collisions
            if environment.check_collision(car):
                assets['collide_sound'].play()
                car.handle_border_collision()
                
            # Check finish
            finish_touch = environment.isEndOfGame(car)
            if finish_touch:
                if finish_touch[1] == 0:
                    car.handle_finishline_collision()
                else:
                    car_moving = False
                    stop_music()
                    state.set_winner(elapsed_time)
                    save_time.save_time(elapsed_time)
                    assets['win_sound'].play()
                    
                    graphics.draw_winner(state)
                    pygame.display.update()
                    
                    waiting_for_restart = True
                    while waiting_for_restart and run:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                waiting_for_restart = False
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    state.reset()
                                    action.reset()
                                    environment.start_time = None
                                    countdown_done = False
                                    car_moving = False
                                    waiting_for_restart = False
                    
        graphics.draw(state, images)

    # Make sure to stop music when game exits
    assets['background_music'].stop()
    pygame.quit()

if __name__ == "__main__":
    main()