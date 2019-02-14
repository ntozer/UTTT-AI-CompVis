from math import inf

from GameAgents import MinimaxAgent


class AlphaBetaAgent(MinimaxAgent):
    def __init__(self, engine, player, depth=4):
        super().__init__(engine=engine, player=player, depth=depth)
        self.agent_type = 'AlphaBeta'

    def minimax(self, node, depth, maximizing_player):
        return self.alpha_beta(node, depth, -inf, inf, maximizing_player)

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.engine.game_state is not None:
            return node
        if maximizing_player:
            max_child = None
            max_value = -inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                child_max = self.minimax(child, depth - 1, False).value
                if max_value <= child_max:
                    max_child = child
                    max_value = child_max
                    node.value = max_value
                alpha = max(alpha, max_value)
                if alpha >= beta:
                    break
            return max_child
        else:
            min_child = None
            min_value = inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                child_min = self.minimax(child, depth - 1, True).value
                if min_value >= child_min:
                    min_child = child
                    min_value = child_min
                    node.value = min_value
                beta = min(beta, min_value)
                if alpha >= beta:
                    break
            return min_child
