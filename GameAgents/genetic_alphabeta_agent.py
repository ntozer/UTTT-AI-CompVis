from GameAgents import AlphaBetaAgent
from GameAgents.evaluator import Evaluator


class GeneticAlphaBetaAgent(AlphaBetaAgent):
    def __init__(self, engine, player, genome, allowed_depth=5):
        super().__init__(engine, player, allowed_depth=allowed_depth)
        self.agent_type = 'Genetic AlphaBeta'
        self.genome = genome

    def compute_position_value(self, engine):
        eval = Evaluator(engine, self.genome)
        return eval.eval()
