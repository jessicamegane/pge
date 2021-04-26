import numpy
import copy

def tournament(population, t_size = 3):
    """Tournament selection function"""
    pool = (numpy.random.choice(population, t_size)).tolist()
    pool.sort(key=lambda i: i['fitness'])
    return copy.deepcopy(pool[0])