import pygame

class Human_Agent():
    def get_action(self):
        keys = pygame.key.get_pressed()
        
        forward = keys[pygame.K_w]
        backward = keys[pygame.K_s]
        left = keys[pygame.K_a]
        right = keys[pygame.K_d]
        
        if forward and left:
            return 5  # forward-left
        elif forward and right:
            return 6  # forward-right
        elif backward and left:
            return 7  # backward-left
        elif backward and right:
            return 8  # backward-right
        elif forward:
            return 1  # forward
        elif backward:
            return 2  # backward
        elif left:
            return 3  # left
        elif right:
            return 4  # right
        else:
            return 0  # no movement
