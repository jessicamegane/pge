import numpy
import copy

def mutate(ind, prob_mutation = 0.9):
    """ Mutation function."""
    gen_size = len(ind['genotype'])
    new_gen = copy.deepcopy(ind['genotype'])
    for i in range(gen_size):
        if numpy.random.uniform() < prob_mutation:
            new_gen[i] = numpy.random.uniform()
    
    return {'genotype': new_gen}