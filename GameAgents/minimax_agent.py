from .agent import Agent
from copy import deepcopy
from math import inf


class Node:
    def __init__(self, parent=None, value=0, child_nodes=[], move=None):
        self.value = value
        self.children = child_nodes
        self.parent = parent
        self.move = move


class MinimaxAgent(Agent):

    def __init__(self, engine, depth=3):
        self.engine = engine
        self.depth = depth

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or len(node.children) == 0:
            return node
        if maximizing_player:
            max_child = None
            max_value = -inf
            for child in node.children:
                child_max = self.minimax(child, depth-1, False).value
                if max_value < child_max:
                    max_child = child
                    max_value = child_max
            return max_child
        else:
            min_child = None
            min_value = inf
            for child in node.children:
                child_min = self.minimax(child, depth-1, True).value
                if min_value > child_min:
                    min_child = child
                    min_value = child_min
            return min_child

    def make_move(self, move, engine):
        engine.board[move.x][move.y] = engine.player
        engine.prev_move = move
        engine.update_master_board()
        engine.update_game_state()
        engine.update_player()

    def compute_position_value(self, engine):
        board = engine.board
        master_board = engine.master_board
        player = engine.player
        game_state = engine.game_state
        corners = [0, 2, 6, 8]
        sides = [1, 3, 5, 7]
        value = 0
        # TODO account for adjacent pieces
        for i in range(len(board)):
            for j in range(len(board[0])):
                board_pos = board[i][j]
                if board_pos is not None and master_board[i] is None:
                    for k in [i, j]:
                        if k in corners:
                            value += 1.25 if board_pos == 1 else -1.25
                        elif k in sides:
                            value += 1 if board_pos == 1 else -1
                        else:
                            value += 1.5 if board_pos == 1 else -1.5
        for i in range(len(master_board)):
            if master_board[i] is not None:
                if i in sides:
                    value += 10 if player == 1 else -10
                elif i in corners:
                    value += 12.5 if player == 1 else -12.5
                else:
                    value += 15 if player == 1 else -15
        if game_state is not None:
            if game_state == 0:
                value = 0
            else:
                value = inf if game_state == 1 else -inf
        return value

    def construct_value_tree(self, node, engine, depth):
        if node.move is not None:
            self.make_move(node.move, engine)
        node.value = self.compute_position_value(engine)
        if depth == 0 or engine.game_state is not None:
            return
        for move in engine.get_valid_moves():
            child = Node(parent=node, move=move)
            node.children.append(child)
        for child in node.children:
            self.construct_value_tree(child, deepcopy(engine), depth-1)

    def compute_next_move(self):
        engine_copy = deepcopy(self.engine)
        root = Node()
        self.construct_value_tree(root, engine_copy, self.depth)
        node = self.minimax(root, self.depth, True)
        return node.move
