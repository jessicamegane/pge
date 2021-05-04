import sys
import copy
import numpy
from tqdm import tqdm
import core.logger as logger
import core.grammar as grammar
from core.operators.mutation import mutate
from core.operators.crossover import crossover
from core.operators.selection import tournament
from core.genotype_generator import (
    float_genotype,
    int_genotype
)
from core.mapping_func import (
    probabilistic_mapping,
    mod_mapping
)
from core.parameters import params
from core.update_probs.update import update_probs
from core.parameters import (
    params,
    set_parameters
)

def setup():
    set_parameters(sys.argv[1:])
    logger.save_parameters()
    grammar.set_path(params['GRAMMAR'])
    grammar.read_grammar()
    numpy.random.seed(params['SEED'])

def mapping_function(genotype):
    """ Genotype-phenotype mapping function. Returns the phenotype and a counter.
    The counter stores the number of times each production rule was expanded. 
    The counter is later used on the function to update the PCFG's probabilities."""
    start = grammar.get_start()
    phenotype = [start]

    ind_pointer = 0
    wrap_counter = 0
    pos = 0
    gram_counter = copy.deepcopy(grammar.get_counter())
    while pos < len(genotype):
        if (pos >= len(genotype) - 1 and wrap_counter < params['MAX_WRAPS']):
            wrap_counter += 1
            pos = 0
        elif wrap_counter == params['MAX_WRAPS']:
            # individuo invalido
            break
        
        codon = genotype[pos]
        symbol = phenotype.pop(ind_pointer)

        productions = grammar.get_dict[symbol]     # get rules from symbol NT

        if params['PGE']:
            idx_selected_rule = probabilistic_mapping(codon, productions)
        else:
            idx_selected_rule = mod_mapping(codon, productions)

        gram_counter[symbol][idx_selected_rule] += 1

        # append at the beggining of the list
        p = ind_pointer
        for prod in productions[idx_selected_rule][0]:
            phenotype.insert(p,prod)    # append selected production
            p += 1
        if grammar.is_individual_t(phenotype):
            break
        else:
            for _ in range(ind_pointer, len(phenotype)):
                if grammar.is_NTerminal(phenotype[ind_pointer]):
                    break
                else:
                    ind_pointer += 1
        pos += 1
    return phenotype, gram_counter


def init_population():
    """ Function to initialise the population."""
    population = []
    while len(population) < params['POP_SIZE']:
        if params['PGE']:
            gen = float_genotype(params['SIZE_GENOTYPE'])
        else:
            gen = int_genotype(params['SIZE_GENOTYPE'], params['SIZE_CODON'])
        population.append({'genotype': gen})
    return population


def evaluate(evaluation_function, population):
    """ Evaluation function. This function calls the evaluation function of the chosen problem.
        The individual's genotype is mapped before evaluating."""
    for ind in tqdm(population):
        ind['phenotype'], ind['gram_counter'] = mapping_function(ind['genotype'])
        trn_error, tst_error = evaluation_function(ind['phenotype'])
        ind['fitness'] = trn_error
        ind['tst_error'] = tst_error


def evolutionary_algorithm(evaluation_function):
    setup()
    population = init_population()
    evaluate(evaluation_function, population)
    best_overall = {}
    flag = False
    for it in range(0, params['GENERATIONS']):
        
        population.sort(key=lambda x: x['fitness'])

        if population[0]['fitness'] <= best_overall.setdefault('fitness', evaluation_function.invalid_fitness):
            best_overall = copy.deepcopy(population [0])
        
        if params['PGE']:
            if not flag:
                update_probs(best_overall, params['LEARNING_FACTOR'], grammar)
            else:
                update_probs(best_generation, params['LEARNING_FACTOR'], grammar)
            flag = not flag

        logger.evolution_progress(it, population, best_overall, grammar)

        new_population = []
        while (len(new_population) < params['POP_SIZE'] - params['ELITISM']):
            ni = tournament(population, params['T_SIZE'])
            if numpy.random.uniform() < params['PROB_CROSSOVER']:
                p1 = tournament(population, params['T_SIZE'])
                p2 = tournament(population, params['T_SIZE'])
                ni = crossover(p1, p2, params['NR_CUTS'])
            else:
                ni = tournament(population, params['T_SIZE'])

            ni = mutate(ni, params['PROB_MUTATION'])

            new_population.append(ni)

        # This part of the code is for saving the best individual of the current generation, without the elitists
        evaluate(evaluation_function, new_population)
        new_population.sort(key=lambda x: x['fitness'])

        best_generation = copy.deepcopy(new_population[0])

        evaluate(evaluation_function, population[:params['ELITISM']])
        new_population += population[:params['ELITISM']]

        if params['ADAPTIVE']:
            params['LEARNING_FACTOR'] += params['ADAPTIVE_INCREMENT']

        population = new_population

