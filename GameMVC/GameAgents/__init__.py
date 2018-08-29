from .agent import Agent
from .random_agent import RandomAgent

agent_types = ['random', 'minimax', 'reinforcment']

__all__ = ['RandomAgent', 'agent_types']