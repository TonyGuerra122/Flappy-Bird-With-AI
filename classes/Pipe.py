import pygame
import random
from utils import get_image

class Pipe:
    DISTANCE = 200
    SPEED = 5
    BASE_IMAGE = get_image('pipe.png', True)
    TOP_IMAGE = pygame.transform.flip(BASE_IMAGE, False, True)
  
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.base_pos = 0
        self.has_passed = False
        self.__set_height()
        
    def __set_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.TOP_IMAGE.get_height()
        self.base_pos = self.height + self.DISTANCE
        
    def move(self):
        self.x -= self.SPEED
        
    def draw(self, screen):
        screen.blit(self.TOP_IMAGE, (self.x, self.top_pos))
        screen.blit(self.BASE_IMAGE, (self.x, self.base_pos))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_IMAGE)
        base_mask = pygame.mask.from_surface(self.BASE_IMAGE)
        
        top_distance = (self.x - bird.x, self.top_pos - round(bird.y))
        base_distance = (self.x - bird.x, self.base_pos - round(bird.y))
        
        top_collision_point = bird_mask.overlap(top_mask, top_distance)
        base_collision_point = bird_mask.overlap(base_mask, base_distance)
        
        return top_collision_point or base_collision_point