import numpy

def float_genotype(size_genotype):
    """ Function that generates the genotype, that is a float list."""
    gen = []
    for _ in range(size_genotype):
        gen.append(numpy.random.uniform())
    return gen

def int_genotype(size_genotype, size_codon):
    """ Function that generates the genotype, that is a integer list in the domain [0,size_codon]."""
    gen = []
    for _ in range(size_genotype):
        gen.append(numpy.random.randint(0, size_codon))
    return gen