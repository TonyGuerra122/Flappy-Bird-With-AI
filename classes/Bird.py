import pygame
from functions.utils import get_image

class Bird:
    IMAGES = [get_image('bird1.png', True), get_image('bird2.png', True), get_image('bird3.png', True)]
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMAGES[0]
        
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y
        
    def move(self):
        # calcular o deslocamento
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time
        
        # restringir o deslocamento
        if displacement > 16: displacement = 16
        elif displacement < 0 : displacement -= 2
        
        self.y += displacement
        
        # o angulo do passáro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION: self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90: self.angle -= self.SPEED_ROTATION
    
    def draw(self, screen):
        # definir a imagem do passáro a ser usada
        self.image_count += 1
        
        if self.image_count < self.ANIMATION_TIME: self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2: self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3: self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4: self.image = self.IMAGES[1]
        elif self.image_count >= self.ANIMATION_TIME * 4 + 1: 
            self.image = self.IMAGES[0]
            self.image_count = 0
    
        # se o passáro estiver caindo, ele não irá bater as asas
        if self.angle <= -80: 
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2
        
        # desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        center_image_pos = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=center_image_pos)
        screen.blit(rotated_image, rectangle.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)