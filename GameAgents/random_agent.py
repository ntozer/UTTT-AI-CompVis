import random
from .agent import Agent

class RandomAgent(Agent):

    def __init__(self):
        pass
    
    def compute_next_move(self, board, valid_moves):
        if len(valid_moves) > 1:
            return valid_moves[random.randint(0, len(valid_moves)-1)]
        elif len(valid_moves) == 1:
            return valid_moves[0]