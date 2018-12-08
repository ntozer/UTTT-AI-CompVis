from .agent import Agent
from copy import deepcopy
from random import randint


class Node():
    def __init__(self, parent, value, child_nodes):
        self.value = value
        self.children = child_nodes
        self.parent = parent


class MinimaxAgent(Agent):

    def __init__(self, engine):
        self.engine = engine

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or len(node.children) == 0:
            return node.value
        if maximizing_player:
            for child in node.children:
                value = max(child.value, self.minimax(child, depth-1, False))
            return value
        else:
            for child in node.children:
                value = min(child.value, self.minimax(child, depth-1, True))
            return value

    def make_move(self, move):
        self.engine.board[move.x][move.y] = self.engine.player
        self.engine.prev_move = move
        self.engine.update_master_board()
        self.engine.update_game_state()
        self.engine.update_player()

    def compute_position_value(self):
        board = self.engine.board
        master_board = self.engine.master_board
        player = self.engine.player
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

        return value

    def construct_value_tree(self, node, depth):
        node.value = self.compute_position_value(self.engine.board)
        if depth == 0:
            return node
        else:
            for move in self.engine.get_valid_moves():
                self.make_move(move)
                node.children.append(self.construct_value_tree(Node(None, []), self.engine, depth-1))
                return node

    def compute_next_move(self):
        depth = 4
        engine_copy = deepcopy(self.engine)
        head_node = self.construct_value_tree(Node(None, []), engine_copy, depth)
        value = self.minimax(head_node, depth, True)
