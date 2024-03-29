from functions.utils import get_image

class Ground:
    IMAGE = get_image('base.png', True)
    SPEED = 5
    WIDTH = IMAGE.get_width()
    
    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WIDTH
    
    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED
        
        if self.x0 + self.WIDTH < 0: self.x0 = self.x1 + self.WIDTH
        if self.x1 + self.WIDTH < 0: self.x1 = self.x0 + self.WIDTH
    
    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x0, self.y))
        screen.blit(self.IMAGE, (self.x1, self.y))