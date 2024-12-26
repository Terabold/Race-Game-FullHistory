import pygame

def blit_rotate_center(game, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(topleft = top_left).center)
    game.blit(rotated_image, new_rect.topleft)

def font_scale(size):
    return pygame.font.Font(r'fonts\PressStart2P-Regular.ttf', size)