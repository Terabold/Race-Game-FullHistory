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

    def _move_and_play_sound(self, assets, forward):
        """Handles forward or backward movement and sound effects."""
        if forward:
            self.car.move_forward()
        else:
            self.car.move_backward()

        # Play acceleration sound, then stop it (if needed)
        assets['acc'].play()
        assets['acc'].stop()

        # Play driving sound
        assets['drive'].set_volume(0.5)
        assets['drive'].play(loops=-1)  # Play the drive sound continuously while moving

    def _play_reduce_sound(self, assets):
        """Handles reducing speed and playing reduce sound."""
        assets['reduce'].set_volume(0.5)
        assets['reduce'].play()
        assets['reduce'].stop()

    def handle_input(self, keys, assets):
        moved = False
        if keys[pygame.K_w]:
            self.car.move_forward()
            moved = True
            assets['drive'].set_volume(0.5)
            assets['acc'].play()
            assets['acc'].stop()
            assets['drive'].play()
        if keys[pygame.K_s]:
            self.car.move_backward()
            moved = True
            assets['drive'].set_volume(0.5)
            assets['acc'].play()
            assets['acc'].stop()
            assets['drive'].play()
        if keys[pygame.K_a]:
            self.car.rotate(left=True)
        if keys[pygame.K_d]:
            self.car.rotate(right=True)
                    
        if not moved:
            self.car.reduce_speed()
            assets['reduce'].play()
            assets['reduce'].stop()

    def reset(self):
        self.car.reset()
        


        
        
