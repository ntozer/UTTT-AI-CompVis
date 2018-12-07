from .agent import Agent
from .random_agent import RandomAgent

agent_types = ['random', 'minimax', 'montecarlo', 'alphazero']

__all__ = ['RandomAgent', 'agent_types']