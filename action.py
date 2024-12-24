import pygame
class Action:
    def __init__(self, car):
        self.reset_requested = False
        self.car = car
        self.waiting_for_restart = False

    def handle_restart(self):
        self.reset_requested = True
        return self.reset_requested

    def handle_events(self, run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.handle_restart()

        return run

    def reset(self):
        self.car.reset()
        
    def handle_input(self, keys, ):
        moved = False

        if keys[pygame.K_w]:
            self.car.move_forward()
            moved = True

        if keys[pygame.K_s]:
            self.car.move_backward()
            moved = True

        if keys[pygame.K_a]:
            self.car.rotate(left=True)

        if keys[pygame.K_d]:
            self.car.rotate(right=True)
                    
        if not moved:
            self.car.reduce_speed()

    
        


        
        
