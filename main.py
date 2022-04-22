import random

class Bandit:
    def __init__(self, base=10):
        self.base = base
    
    def run(self):
        return self.base * random.random()


def generate_bandits(n):
    bandits = []
    for i in range(n):
        b = Bandit(base=random.randint(1, 100))
        bandits.append(b)
    
    return bandits

        