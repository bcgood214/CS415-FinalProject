# Benjamin Good
# 2022-04-25
# CS 415
import random
from gen_epsilon import *

class Bandit:
    def __init__(self, base=10):
        self.base = base
    
    def run(self):
        return self.base * (random.random() * 2)

class Agent:

    def __init__(self, bandits):
        self.options = []
        # initialize each estimate to 500, with 0 for the number of rewards
        for bandit in bandits:
            self.options.append([bandit, 1, 0])
        self.score = 0
    
    def getbest(self):
        max = -1
        self.pick = None
        for option in self.options:
            if option[1] > max:
                max = option[1]
                self.pick = option
    
    def getrand(self):
        self.pick = random.choice(self.options)




def generate_bandits(n):
    # print("Generating bandits")
    bandits = []
    for i in range(n):
        b = Bandit(base=random.randint(1, 500))
        # print(b.base)

        bandits.append(b)
    
    return bandits

def generate_pool(poolsize):
    pool = []
    for i in range(poolsize):
        pool.append(gen_ind(Node(), no_term=True))
    
    return pool

def run_testbed(epsilon, testbed):
    agent = Agent(testbed)
    for i in range(1000):
        if random.random() < epsilon:
            agent.getrand()
        else:
            agent.getbest()
        
        reward = agent.pick[0].run()
        agent.pick[2] += 1
        if agent.pick[2] == 1:
            agent.pick[1] = reward
        else:
            agent.pick[1] = agent.pick[1] + 1/(agent.pick[2]) * (reward - agent.pick[1])
        """ agent.pick[2] += 1
        # computing the estimate
        agent.pick[1] = agent.pick[1] + 1/(agent.pick[2]) * (reward - agent.pick[1]) """
        agent.score += reward
    
    # for_printing = [[option[1], option[2]] for option in agent.options]
    # print(for_printing)
    
    return agent.score




def test_epsilon(epsilon, testbed):
    # testbed = generate_bandits(testbed_size)

    score = run_testbed(epsilon, testbed)


    # may just remove the 'score' variable
    return score

def get_fittest(pool):
    # print(pool)
    fittest = pool[0][0]
    fittest_val = pool[0][1]
    # print("First ind: {}".format(fittest_val))
    for ind in pool:
        if ind[1] > fittest_val:
            fittest = ind[0]
            fittest_val = ind[1]
    
    # print(fittest_val)
    
    return fittest

def eval(ind, testbed):
    epsilon = ind.run()
    # create a 10-armed testbed for evaluatiing epsilon
    epsilon_score = test_epsilon(epsilon, testbed)

    return epsilon_score



def main(gens):
    pool = generate_pool(40)
    # create a 10-armed testbed
    testbed = generate_bandits(100)
    
    for i in range(gens):
        fitness_pool = []
        next_gen = []
        # print("Pool #{}".format(i))

        for ind in pool:
            ind_score = eval(ind, testbed)
            fitness_pool.append([ind, ind_score])
            # print(ind.run())
        
        fittest = get_fittest(fitness_pool)
        
        inds = [elem[0] for elem in fitness_pool]
        scores = [elem[1] for elem in fitness_pool]
        for j in range(len(pool) - 1):
            parents = random.choices(inds, weights=scores, k=2)
            # print("Parents: {}, {}".format(parents[0].run(), parents[1].run()))
            child = recombine(parents[0], parents[1])
            next_gen.append(child)
        
        next_gen.append(fittest)
        # print("Fittest: {}".format(fittest.run()))

        pool = next_gen
    
    fitness_pool = []
    
    for ind in pool:
            ind_score = eval(ind, testbed)
            fitness_pool.append([ind, ind_score])
            # print("Epsilon: {}\nScore: {}".format(ind.run(), eval(ind, testbed)))
    
    return get_fittest(fitness_pool)

if __name__ == "__main__":
    ind = main(50)
    print(ind.run())