import pygame
from Constants import *

class Ground (pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(GRASS).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
