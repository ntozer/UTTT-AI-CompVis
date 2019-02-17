import random
from copy import deepcopy
from multiprocessing import Process, Lock, Queue, Manager

from GameMVC import Engine
from GameAgents import GeneticAlphaBetaAgent


class Simulator:
    def __init__(self, num_generations=10, population_size=30, num_parents=4, epsilon=0.1, parallel=False):
        self.engine = Engine()
        self.num_generations = num_generations
        self.population_size = population_size
        self.num_parents = num_parents
        self.epsilon = epsilon
        self.population = []
        self.matchups = []
        self.parents = []
        self.breed_method = 'randrange'
        self.genome_len = 11
        self.gen_num = 0
        self.parallel = parallel
        if self.parallel:
            self.manager = Manager()
            self.matchups = Queue()
            self.population = self.manager.list()

    def init_sample(self, genome):
        if self.parallel:
            return self.manager.dict({
                'genome': genome,
                'wins': 0,
                'games': 0,
                'record': 0
            })
        return {
            'genome': genome,
            'wins': 0,
            'games': 0,
            'record': 0
        }

    def handle_next_move(self, engine, agent1, agent2):
        move = None
        if engine.player == 1:
            move = agent1.compute_next_move()
        elif engine.player == 2:
            move = agent2.compute_next_move()
        engine.make_move(move)

    def build_random_sample(self):
        genome = []
        for i in range(self.genome_len):
            genome.append(random.randrange(0, 10000) / 1000)
        # if self.parallel:
            # return self.manager.Sample(Sample(genome))
        return self.init_sample(genome)

    def build_breeded_sample(self):
        genome = []
        for i in range(self.genome_len):
            mutate = (random.randrange(0, 100) / 100) < self.epsilon
            p1 = self.parents.pop(random.randrange(0, len(self.parents)))
            p2 = self.parents[random.randrange(0, len(self.parents))]
            self.parents.append(p1)
            p1_gene = p1['genome'][i]
            p2_gene = p1['genome'][i]
            if mutate:
                genome.append(random.randrange(0, 10000) / 100)
            elif self.breed_method == 'randrange':
                if p1_gene > p2_gene:
                    genome.append(random.randrange(int(p2_gene * 100), int(p1_gene * 100)) / 100)
                elif p1_gene < p2_gene:
                    genome.append(random.randrange(int(p1_gene * 100), int(p2_gene * 100)) / 100)
                else:
                    genome.append(p1_gene)
            elif self.breed_method == 'weighted_sum':
                p1_weight = p1.record / (p1.record + p2.record)
                p2_weight = p2.record / (p1.record + p2.record)
                gene = p1_gene * p1_weight + p2_gene * p2_weight
                genome.append(gene)
        # if self.parallel:
            # return self.manager.Sample(Sample(genome))
        return self.init_sample(genome)

    def generate_population(self):
        self.population = []
        if self.parallel:
            self.population = Manager().list()
        if len(self.parents) == 0:
            for i in range(self.population_size):
                sample = self.build_random_sample()
                self.population.append(sample)
        else:
            for i in range(self.population_size):
                sample = self.build_breeded_sample()
                self.population.append(sample)

    def select_parents(self):
        self.population = sorted(self.population, key=lambda k: k['record'], reverse=True)
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
            for i in range(pop_size-1):
                for j in range(pop_size // 2):
                    matchups.append((self.population[j], self.population[pop_size-2-j]))
                self.population = rotate(self.population)
        self.matchups = matchups

    def play_match(self, matchup, lock=None):
        engine_copy = deepcopy(self.engine)
        p1 = matchup[0]
        p1_agent = GeneticAlphaBetaAgent(engine_copy, 1, p1['genome'], allowed_depth=4, simulation=True)
        p2 = matchup[1]
        p2_agent = GeneticAlphaBetaAgent(engine_copy, 2, p2['genome'], allowed_depth=4, simulation=True)
        while engine_copy.game_state is None:
            self.handle_next_move(engine_copy, p1_agent, p2_agent)
        if lock is not None:
            lock.acquire()
        p1['games'] += 1
        p2['games'] += 1
        if engine_copy.game_state == 0:
            p1['wins'] += 0.5
            p2['wins'] += 0.5
        elif engine_copy.game_state == 1:
            p1['wins'] += 1
        else:
            p2['wins'] += 1
        p1['record'] = p1['wins'] / p1['games']
        p2['record'] = p2['wins'] / p2['games']
        if lock is not None:
            lock.release()

    def output_parent_genomes(self, generation):
        print(f'Best Genomes from Generation {generation}')
        for parent in self.parents:
            print(f'{list(map(lambda x: round(x, 4), parent["genome"]))}\t{round(parent["record"], 3)}')

    def run(self):
        if self.parallel:
            self.run_parallel()
        else:
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
            self.output_parent_genomes(self.gen_num)


if __name__ == '__main__':
    sim = Simulator(20, 15, 4, 0.1, parallel=True)
    sim.run()

