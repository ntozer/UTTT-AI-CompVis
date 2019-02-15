import time
from math import inf

from GameAgents import MinimaxAgent


class CacheObj:
    def __init__(self, val, depth, node=None):
        self.val = val
        self.depth = depth
        self.best = node 


class AlphaBetaAgent(MinimaxAgent):
    def __init__(self, engine, player, compute_time=1):
        super().__init__(engine=engine, player=player)
        self.agent_type = 'AlphaBeta'
        self.compute_time = compute_time
        self.cache = {}

    def minimax(self, node, depth, maximizing_player):
        start_time = time.time()
        max_depth = 1
        while True:
            depth_start = time.time()
            child, _ = self.alpha_beta(node, max_depth, -inf, inf, maximizing_player)
            print(f'a-B @ depth: {max_depth}: {time.time() - depth_start}s')
            if time.time() - start_time > self.compute_time:
                break
            max_depth += 1
        print(f'Max Depth {max_depth}')
        return child, _

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.engine.game_state is not None:
            return node, node.value
        node_key = self.to_key(node.engine.board)
        moves = node.engine.get_valid_moves()
        cache_keys = self.cache.keys()
        if maximizing_player:
            max_child = None
            max_value = -inf
            # if node_key in self.cache.keys():
            #     best_move = self.cache[node_key].best.move
            #     # moves.remove(best_move)
            #     moves = [best_move, *moves]
            for move in moves:
                child = self.build_child(parent=node, move=move)
                child_key = self.to_key(child.engine.board)
                if child_key in cache_keys and depth <= self.cache[child_key].depth:
                    child_max = self.cache[child_key].val
                else:
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
            if node_key not in cache_keys or depth > self.cache[node_key].depth:
                self.cache[node_key] = CacheObj(max_value, depth, max_child)
            return max_child, max_value
        else:
            min_child = None
            min_value = inf
            moves = node.engine.get_valid_moves()
            # if node_key in self.cache.keys():
            #     best_move = self.cache[node_key].best.move
            #     # moves.remove(best_move)
            #     moves = [best_move, *moves]
            for move in moves:
                child = self.build_child(parent=node, move=move)
                child_key = self.to_key(child.engine.board)
                if child_key in cache_keys and depth <= self.cache[child_key].depth:
                    child_min = self.cache[child_key].val
                else:
                    _, child_min = self.alpha_beta(child, depth - 1, alpha, beta, True)
                child.engine.undo_move(child.move)
                if child_min < min_value:
                    min_child = child
                    min_value = child_min
                    node.value = min_value
                if min_value <= alpha:
                    break
                if min_value < beta:
                    beta = min_value
            if node_key not in cache_keys or depth > self.cache[node_key].depth:
                self.cache[node_key] = CacheObj(min_value, depth, min_child)
            return min_child, min_value

    def to_key(self, board):
        return tuple(tuple(board[i]) for i in range(9))
