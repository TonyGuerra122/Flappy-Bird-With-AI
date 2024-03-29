import neat
from functions.utils import get_path_from_files

class AI:
    
    AI_CONFIG = get_path_from_files("ai_config.txt")
    
    def __init__(self):
        self.generation = 0
        
        config = neat.config.Config(neat.DefaultGenome,
                                        neat.DefaultReproduction,
                                        neat.DefaultSpeciesSet,
                                        neat.DefaultStagnation,
                                        self.AI_CONFIG
                                        )
        
        self.population = neat.Population(config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.population.add_reporter(neat.StatisticsReporter())
        
    def run_population(self, fitness_function, generations=None):
        self.population.run(fitness_function, generations)
        
    
        