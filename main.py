import pygame
from utils import get_image
from classes.Bird import Bird
from classes.Ground import Ground
from classes.Pipe import Pipe

# Constantes do game
WIDTH_SCREEN = 500
HEIGHT_SCREEN = 800
BACKGROUND_IMAGE = get_image('bg.png', True)

# Configuração de font
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

# Função para desenhar a tela
def draw_screen(screen, birds, pipes, ground, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    
    text = POINTS_FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
    
    screen.blit(text, (WIDTH_SCREEN - 10 - text.get_width(), 10))
    ground.draw(screen)
    
    pygame.display.update()

# Função principal
def main():
    birds = [Bird(230, 350)]
    ground = Ground(730)
    pipes = [Pipe(700)]
    
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    points = 0
    clock = pygame.time.Clock()   
    
    is_running = True
    
    while is_running:
        clock.tick(30)
        
        # interação com o usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
            
        # mover as coisas
        for bird in birds:
            bird.move()
                
        ground.move()
        
        add_pipe = False
        
        remove_pipe = []
        
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird): birds.pop(i)
                if not pipe.has_passed and bird.x > pipe.x:
                    pipe.has_passed = True
                    add_pipe = True
            pipe.move()
            
            if pipe.x + pipe.TOP_IMAGE.get_width() < 0:
                remove_pipe.append(pipe)
        
        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
            
            for pipe in remove_pipe:
                pipes.remove(pipe)
                
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0: birds.pop(i)
        
        draw_screen(screen, birds, pipes, ground, points)
        
if __name__ == '__main__': main()