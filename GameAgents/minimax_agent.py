from .agent import Agent
from copy import deepcopy
from random import randint

class Node():

    def __init__(self, value, child_nodes):
        self.value = value
        self.children = child_nodes


class MinimaxAgent(Agent):

    def __init__(self):
        pass


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

    
    def make_move(self, move, engine):
        engine.board[move.x][move.y] = engine.player
        engine.prev_move = move
        engine.update_master_board()
        engine.update_game_state()
        engine.update_player()


    def compute_position_value(self, board):
        # setup NN for predicting board state value
        return randint(-10, 10)


    def construct_value_tree(self, node, engine, depth):
        node.value = self.compute_position_value(engine.board)
        if depth == 0:
            return node
        else:
            for move in engine.get_valid_moves():
                self.make_move(move, engine)
                node.children.append(self.construct_value_tree(Node(None, []), engine, depth-1))
                return node


    def compute_next_move(self, engine):
        depth = 4
        engine_copy = deepcopy(engine)
        head_node = self.construct_value_tree(Node(None, []), engine_copy, depth)
        value = self.minimax(head_node, depth, True)
