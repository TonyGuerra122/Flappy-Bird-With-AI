import pygame
import neat
from functions.utils import get_image
from classes.Bird import Bird
from classes.Pipe import Pipe
from classes.Ground import Ground

class Game:
    # Constantes do game
    WIDTH_SCREEN = 500
    HEIGHT_SCREEN = 800
    BACKGROUND_IMAGE = get_image('bg.png', True)
    
    # Configuração de fonte
    pygame.font.init()
    POINTS_FONT = pygame.font.SysFont('arial', 50)
    
    def __init__(self, ai=None):
        self.ai = ai
    
    # Função para desenhar a tela
    def __draw_screen(self, screen, birds, pipes, ground, points):
        screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        
        for bird in birds:
            bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        
        text = self.POINTS_FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
        screen.blit(text, (self.WIDTH_SCREEN - 10 - text.get_width(), 10))
        
        if self.ai:
            text = self.POINTS_FONT.render(f"Geração: {self.ai.generation}", 1, (255, 255, 255))
            screen.blit(text, (10, 10))
        
        ground.draw(screen)
        
        pygame.display.update()
    
    # Função para iniciar o game
    def start(self, genomes=None, config=None): # Fitness Function
        if self.ai: 
            self.ai.generation += 1
            birds = []
            genome_list = []
            net_list = []

            for _, genome in genomes:
                net = neat.nn.FeedForwardNetwork.create(genome, config)
                
                genome.fitness = 0
                
                net_list.append(net)
                genome_list.append(genome)
                birds.append(Bird(230, 350))
        else: birds = [Bird(230, 350)]
        ground = Ground(730)
        pipes = [Pipe(700)]
        
        screen = pygame.display.set_mode((self.WIDTH_SCREEN, self.HEIGHT_SCREEN))
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
                if not self.ai: 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            for bird in birds:
                                bird.jump()
            
            pipe_index = 0
            
            if len(birds) > 0:
                # descobrir qual cano olhar
                
                if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].TOP_IMAGE.get_width()):
                    pipe_index = 1
                    
            else:
                is_running = False
                break
                            
            # mover as coisas
            for i, bird in enumerate(birds):
                bird.move()
                
                # caso a ia esteja ativada
                if self.ai:
                    # aumentar a fitness do passáro
                    genome_list[i].fitness += 0.1
                    output = net_list[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].base_pos)))
                    
                    # 1- e 1 -> se o output for > 0.5 então o passáro pula
                    if output[0] > 0.5:
                        bird.jump()
                    
            ground.move()
            
            add_pipe = False
            
            remove_pipe = []
            
            for pipe in pipes:
                
                for i, bird in enumerate(birds):
                    
                    if pipe.collide(bird): 
                        birds.pop(i)
                        
                        if self.ai:
                            genome_list[i].fitness -= 1
                            genome_list.pop(i)
                            net_list.pop(i) 
                    
                    if not pipe.has_passed and bird.x > pipe.x:
                        pipe.has_passed = True
                        add_pipe = True
                
                pipe.move()
                
                if pipe.x + pipe.TOP_IMAGE.get_width() < 0:
                    remove_pipe.append(pipe)
            
            if add_pipe:
                points += 1
                pipes.append(Pipe(600))
                
                if self.ai:
                    for genome in genome_list:
                        genome.fitness += 5
                
            for pipe in remove_pipe:
                pipes.remove(pipe)
                    
            for i, bird in enumerate(birds):
                
                if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0: 
                    birds.pop(i)
                    
                    if self.ai:
                        genome_list.pop(i)
                        net_list.pop(i)
            
            self.__draw_screen(screen, birds, pipes, ground, points)