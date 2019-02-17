import random
from copy import deepcopy
from multiprocessing import Process, Lock, Queue
from multiprocessing.managers import BaseManager

from GameMVC import Engine
from GameAgents import GeneticAlphaBetaAgent


class Sample:
    def __init__(self, agent):
        self.agent = agent
        self.wins = 0
        self.games = 0
        self.record = None

    def __lt__(self, other):
        return self.record < other.record

    def __le__(self, other):
        return self.record <= other.record


class Simulator:
    def __init__(self, num_generations=10, population_size=30, num_parents=4, epsilon=0.1):
        self.engine = Engine()
        self.num_generations = num_generations
        self.population_size = population_size
        self.num_parents = num_parents
        self.epsilon = epsilon
        self.population = []
        self.matchups = []
        self.parents = []
        self.breed_method = 'randrange'

        # multiprocessin stuff
        BaseManager.register('Sample', Sample)
        self.manager = BaseManager()
        self.manager.start()

    def handle_next_move(self, engine, agent1, agent2):
        move = None
        if engine.player == 1:
            move = agent1.compute_next_move()
        elif engine.player == 2:
            move = agent2.compute_next_move()
        engine.make_move(move)

    def build_random_sample(self):
        agent = GeneticAlphaBetaAgent(None, None, None, allowed_depth=4, simulation=True)
        genome = []
        for i in range(agent.evaluator.genome_len):
            genome.append(random.randrange(0, 10000) / 1000)
        agent.evaluator.genome = genome
        return Sample(agent)
        # return self.manager.Sample(agent)

    def build_breeded_sample(self):
        agent = GeneticAlphaBetaAgent(None, None, None, allowed_depth=4, simulation=True)
        genome = []
        for i in range(agent.evaluator.genome_len):
            mutate = (random.randrange(0, 100) / 100) < self.epsilon
            p1 = self.parents.pop(random.randrange(0, len(self.parents)))
            p2 = self.parents[random.randrange(0, len(self.parents))]
            self.parents.append(p1)
            p1_gene = p1.agent.evaluator.genome[i]
            p2_gene = p2.agent.evaluator.genome[i]
            if mutate:
                genome.append(random.randrange(0, 10000) / 1000)
            elif self.breed_method == 'randrange':
                if p1_gene > p2_gene:
                    genome.append(random.randrange(int(p2_gene * 10000), int(p1_gene * 10000)) / 1000)
                elif p1_gene < p2_gene:
                    genome.append(random.randrange(int(p1_gene * 10000), int(p2_gene * 10000)) / 1000)
                else:
                    genome.append(p1_gene)
            elif self.breed_method == 'weighted_sum':
                p1_weight = p1.record / (p1.record + p2.record)
                p2_weight = p2.record / (p1.record + p2.record)
                gene = p1_gene * p1_weight + p2_gene * p2_weight
                genome.append(gene)
        agent.evaluator.genome = genome
        return Sample(agent)
        # return self.manager.Sample(agent)

    def generate_population(self):
        self.population = []
        if len(self.parents) == 0:
            for i in range(self.population_size):
                sample = self.build_random_sample()
                self.population.append(sample)
        else:
            for i in range(self.population_size):
                sample = self.build_breeded_sample()
                self.population.append(sample)

    def select_parents(self):
        self.population.sort(reverse=True)
        self.parents = self.population[:self.num_parents]

    def generate_matchups(self):
        def rotate(n):
            return n[1:] + n[:1]
        matchups = []
        pop_size = self.population_size
        if pop_size % 2 == 0:
            for i in range(pop_size-1):
                for j in range(pop_size // 2):
                    matchups.append((self.population[j], self.population[pop_size-1-j]))
                constant = self.population[0]
                self.population.pop(0)
                self.population = rotate(self.population)
                self.population = [constant, *self.population]

        else:
            for i in range(self.population-1):
                for j in range(pop_size // 2):
                    matchups.append((self.population[j], self.population[pop_size-2-j]))
                self.population= rotate(self.population)
        self.matchups = matchups

    def play_match(self, matchup, lock=None):
        engine_copy = deepcopy(self.engine)
        p1 = matchup[0]
        p1.agent.player = 1
        p1.agent.engine = engine_copy
        p2 = matchup[1]
        p2.agent.player = 2
        p2.agent.engine = engine_copy
        while engine_copy.game_state is None:
            self.handle_next_move(engine_copy, p1.agent, p2.agent)
        if lock is not None:
            lock.acquire()
        p1.games += 1
        p2.games += 1
        if engine_copy.game_state == 0:
            p1.wins += 0.5
            p2.wins += 0.5
        elif engine_copy.game_state == 1:
            p1.wins += 1
        else:
            p2.wins += 1
        p1.record = p1.wins / p1.games
        p2.record = p2.wins / p2.games
        p1.agent.player = None
        p1.agent.engine = None
        p2.agent.player = None
        p2.agent.engine = None
        if lock is not None:
            lock.release()

    def output_parent_genomes(self, generation):
        print(f'Best Genomes from Generation {generation}')
        for parent in self.parents:
            print(f'{list(map(lambda x: round(x, 4), parent.agent.evaluator.genome))}\t{round(parent.record, 3)}')

    def run(self):
        for i in range(self.num_generations):
            print(f'\nBEGINNING GENERATION {i}')
            self.generate_population()
            self.generate_matchups()
            while len(self.matchups) != 0:
                print(f'Simulations left: {len(self.matchups)} of gen. {i}')
                matchup = self.matchups.pop()
                self.play_match(matchup)
            self.select_parents()
            self.output_parent_genomes(i)

    def do_work(self, matchup_lock, update_lock):
        while True:
            if self.matchups.qsize() == 0:
                break
            matchup_lock.acquire()
            matchup = self.matchups.get()
            print(f'Simulations left: {self.matchups.qsize()} in gen. {self.gen_num}')
            matchup_lock.release()
            self.play_match(matchup, update_lock)

    def run_parallel(self):
        for i in range(self.num_generations):
            self.gen_num = i
            print(f'\nBEGINNING GENERATION {i}')
            self.generate_population()
            self.generate_matchups()
            matchup_lock = Lock()
            update_lock = Lock()
            temp = self.matchups
            self.matchups = Queue()
            for m in temp:
                self.matchups.put(m)
            processes = []
            for i in range(4):
                processes.append(Process(target=self.do_work, args=(matchup_lock, update_lock)))
                processes[i].start()
            for i in range(4):
                processes[i].join()
            self.select_parents()
            self.output_parent_genomes()


if __name__ == '__main__':
    sim = Simulator(20, 20, 4, 0.1)
    sim.run()

