from math import inf

from GameAgents import MinimaxAgent


class AlphaBetaObj:
    def __init__(self, val, node):
        self.val = val
        self.node = node


class AlphaBetaAgent(MinimaxAgent):
    def __init__(self, engine, player, depth=4):
        super().__init__(engine=engine, player=player, depth=depth)
        self.agent_type = 'AlphaBeta'

    def minimax(self, node, depth, maximizing_player):
        return self.alpha_beta(node, depth, -inf, inf, maximizing_player)

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.engine.game_state is not None:
            return node, node.value
        if maximizing_player:
            max_child = None
            max_value = -inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                _, child_max = self.alpha_beta(child, depth-1, alpha, beta, False)
                child.engine.undo_move(child.move)
                if child_max > max_value:
                    max_child = child
                    max_value = child_max
                    node.value = max_value
                if max_value >= beta:
                    break
                if max_value > alpha:
                    alpha = max_value
            return max_child, max_value
        else:
            min_child = None
            min_value = inf
            for move in node.engine.get_valid_moves():
                child = self.build_child(parent=node, move=move)
                _, child_min = self.alpha_beta(child, depth-1, alpha, beta, True)
                child.engine.undo_move(child.move)
                if child_min < min_value:
                    min_child = child
                    min_value = child_min
                    node.value = min_value
                if min_value <= alpha:
                    break
                if min_value < beta:
                    beta = min_value
            return min_child, min_value
