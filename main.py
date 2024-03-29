from classes.Game import Game
from classes.AI import AI

def run_with_ai():
    ai = AI()
    game = Game(ai)
    ai.run_population(game.start, 50)

def run_withoud_ai():
    game = Game()
    game.start()
    
if __name__ == '__main__':
    run_with_ai()
