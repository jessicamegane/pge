import numpy
import copy

def crossover(p1, p2, nr_cuts = 2):
    """ Crossover function. """
    genotype = copy.deepcopy(p1['genotype'])
    gen_size = len(p1['genotype'])
    cuts = []
    while len(cuts) != nr_cuts:
        cutPoint = numpy.random.randint(0,gen_size)
        if cutPoint not in cuts:
            cuts.append(cutPoint)
    cuts.sort()

    partnerGenotype = False
    start = 0
    for i in range(0, nr_cuts):
        if i != 0:
            start = cuts[i-1]
        partnerGenotype = not partnerGenotype
        if partnerGenotype:
            genotype[start:cuts[i]] = p2['genotype'][start:cuts[i]]

    return {'genotype': genotype}