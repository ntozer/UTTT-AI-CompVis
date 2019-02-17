from copy import deepcopy

from GameAgents import AlphaBetaAgent
from GameAgents.evaluator import Evaluator
from GameAgents.minimax_agent import Node


class GeneticAlphaBetaAgent(AlphaBetaAgent):
    def __init__(self, engine, player, genome, compute_time=1, allowed_depth=5, simulation=False):
        super().__init__(engine, player, compute_time, allowed_depth)
        self.agent_type = 'Genetic AlphaBeta'
        self.evaluator = Evaluator(genome)
        self.simulation = simulation

    def compute_position_value(self, engine):
        return self.evaluator.eval(engine)

    def compute_next_move(self):
        self.root = Node(engine=deepcopy(self.engine))
        node, _ = self.minimax(self.root, self.depth, self.player == 1)
        if not self.simulation:
            print(f'{self.agent_type}: {chr(node.move.x + 97)}{node.move.y}, Board Eval: {round(node.value, 4)}')
        return node.move
