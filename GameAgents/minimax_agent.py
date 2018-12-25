from .agent import Agent
from copy import deepcopy
from math import inf
import GameAgents.evaluation_functions


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

    def compute_position_value(self, engine):
        return GameAgents.evaluation_functions.simple_eval(engine)

    def construct_value_tree(self, node, engine, depth):
        if node.move is not None:
            engine.make_move(node.move)
        node.value = self.compute_position_value(engine)
        if depth == 0 or engine.game_state is not None:
            return
        for move in engine.get_valid_moves():
            child = Node(parent=node, move=move)
            child.children = []
            node.children.append(child)
        for child in node.children:
            self.construct_value_tree(child, deepcopy(engine), depth-1)

    def compute_next_move(self):
        engine_copy = deepcopy(self.engine)
        root = Node()
        self.construct_value_tree(root, engine_copy, self.depth)
        node = self.minimax(root, self.depth, True)
        print(f'Minimax Move: {chr(node.move.x + 97)}{node.move.y}')
        return node.move
