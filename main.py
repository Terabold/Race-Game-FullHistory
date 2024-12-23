import pygame
import time
from utils import scale_img, scale_finishline, font_scale
from Agent import Car
from Environment import Environment
from State import State
from action import Action

def main():
    pygame.init()
    
    width, height = 1600, 900 
    game = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Racing Game")
    
    # Load and scale images with proper conversion
    car_img = scale_img(pygame.image.load(r'photo\white-car.png').convert_alpha(), 0.5)
    track_border = pygame.image.load(r'photo\track-stretch-border-2.png').convert_alpha()
    background = pygame.image.load(r'photo\background_menu.jpeg').convert()
    grass = pygame.image.load(r'photo\grass2.jpg').convert()  
    track = pygame.image.load(r'photo\track-stretch.png').convert_alpha()
    finish_line = scale_finishline(pygame.image.load(r'photo\finish.png').convert(), 2)
    finish_line_position = [250, 250]
    
    # Initialize objects
    car = Car(5, 5)
    car.set_image(car_img)
    
    environment = Environment(track, track_border, finish_line, finish_line_position)
    images = environment.setup_images(grass, track)
    
    state = State(car)
    action = Action(car)    
    
    # Game variables
    clock = pygame.time.Clock()
    
    run = True
    car_moving = False
    countdown_done = False
    reset_requested = False

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_requested = True
                    countdown_done = False
                    car_moving = False

        if reset_requested or not countdown_done:
            environment.countdown(game, car, images)
            countdown_done = True
            car_moving = True
            reset_requested = False

        environment.draw(game, images, car)

        # Display FPS and time
        fps_text = font_scale(18).render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        game.blit(fps_text, (10, 10))

        #time display
        if environment.start_time:
            elapsed_time = time.time() - environment.start_time
            timer_text = font_scale(25).render(f"Time: {elapsed_time:.2f} sec", True, (255, 255, 255))
            game.blit(timer_text, (10, height - 40))

        vel_text = font_scale(25).render(f"Vel: {round(car.vel*10, 1):.0f}m/s", 1, (255, 255, 255))
        game.blit(vel_text, (10, height - 45 - timer_text.get_height() ))

        if car_moving:
            # Handle input
            keys = pygame.key.get_pressed()
            moved = False

            if keys[pygame.K_w]:  # Move forward normally
                car.move_forward()
                moved = True
            if keys[pygame.K_s]:  # Move backward normally
                car.move_backward()
                moved = True
            if keys[pygame.K_a]:  # Rotate left normally
                car.rotate(left=True)
            if keys[pygame.K_d]:  # Rotate right normally
                car.rotate(right=True)

            if not moved:
                car.reduce_speed()


            # Check collisions
            if car_moving and environment.check_collision(car):
                car.bounce()

            # Check finish
            finish_touch = environment.check_finish(car)
            if finish_touch:
                if finish_touch[1] == 0:
                    car.bounceextra()
                else:
                    car_moving = False
                    state.set_winner(elapsed_time)
                    winner_text = font_scale(40).render(state.winner, True, (255, 215, 0))
                    restart_text = font_scale(40).render("Press SPACE to play again", True, (0, 255, 0))
                    
                    # Draw winner and restart text
                    game.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - 50))
                    game.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))
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

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()