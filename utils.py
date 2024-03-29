import pygame
import os

def get_image(file, scale2x=False):
    image = pygame.image.load(os.path.join('images', file))
    
    if scale2x: image = pygame.transform.scale2x(image)
        
    return image