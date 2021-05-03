import argparse
import yaml

'''
This was adapted from PonyGE2: https://github.com/PonyGE/PonyGE2
Fenton, M., McDermott, J., Fagan, D., Forstenlechner, S., Hemberg, E., and O'Neill, M. PonyGE2: Grammatical Evolution in Python. arXiv preprint, arXiv:1703.08535, 2017.
'''
""""Algorithm Parameters"""

params = {
    'PARAMETERS': None,
    'RUN': 0,
    'POP_SIZE': 1000,
    'GENERATIONS': 100,
    'ELITISM': 100,
    'T_SIZE': 3,
    'PROB_MUTATION': 0.05,
    'PROB_CROSSOVER': 0.9,
    'NR_CUTS': 1,
    'SIZE_GENOTYPE': 128,
    'SIZE_CODON': 255,
    'MAX_WRAPS': 1,
    'PGE': True,
    'LEARNING_FACTOR': 0.01,
    'ADAPTIVE': False,
    'ADAPTIVE_INCREMENT': 0.001,
    'SEED': 3601294368,
    'SAVE_POP': False,
    'GRAMMAR': 'grammars/5bitparity.bnf',
    'EXPERIMENT_NAME': 'test_pge',
    'PATH': None,
    'VERBOSE': False
}


def load_parameters(file_name=None):
    with open(file_name, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    params.update(cfg)


def set_parameters(arguments):
    # Initialise parser
    parser = argparse.ArgumentParser(
        usage=argparse.SUPPRESS,
        description="Probabilistic Grammatical Evolution code",
    )
    parser.add_argument('--parameters',
                        dest='PARAMETERS',
                        type=str,
                        help='Specifies the parameters file to be used. Must '
                             'include the full file extension. Full file path '
                             'does NOT need to be specified.')
    parser.add_argument('--popsize',
                        dest='POP_SIZE',
                        type=int,
                        help='Specifies the population size.')
    parser.add_argument('--generations',
                        dest='GENERATIONS',
                        type=float,
                        help='Specifies the total number of generations.')
    parser.add_argument('--elitism',
                        dest='ELITISM',
                        type=int,
                        help='Specifies the total number of individuals that should survive in each generation.')
    parser.add_argument('--seed',
                        dest='SEED',
                        type=int,
                        help='Specifies the seed to be used by the random number generator.')
    parser.add_argument('--prob_crossover',
                        dest='PROB_CROSSOVER',
                        type=float,
                        help='Specifies the probability of crossover usage. Float required.')
    parser.add_argument('--prob_mutation',
                        dest='PROB_MUTATION',
                        type=float,
                        help='Specifies the probability of mutation usage. Float required.')
    parser.add_argument('--tsize',
                        dest='TSIZE',
                        type=int,
                        help='Specifies the tournament size for parent selection.')
    parser.add_argument('--grammar',
                        dest='GRAMMAR',
                        type=str,
                        help='Specifies the path to the grammar file.')
    parser.add_argument('--experiment_name',
                        dest='EXPERIMENT_NAME',
                        type=str,
                        help='Specifies the name of the folder where stats are going to be stored.')
    parser.add_argument('--verbose',
                        dest='VERBOSE',
                        type=bool,
                        help='Turns on the verbose output of the program')
    parser.add_argument('--run',
                        dest='RUN',
                        type=int,
                        help='Specifies the run number.')
    parser.add_argument('--pge',
                        dest='PGE',
                        type=bool,
                        help='Specifies if it is to run PGE or the standard GE. '
                        'Boolean required. True: run PGE, False: run GE.')
    parser.add_argument('--learning_factor',
                        dest='LEARNING_FACTOR',
                        type=float,
                        help='Specifies the value of the learning factor used to update the probabilities. '
                            'Float Required.')
    parser.add_argument('--adaptive',
                        dest='ADAPTIVE',
                        type=bool,
                        help='Specifies if it is supposed to run the adaptive version of PGE.')
    parser.add_argument('--adaptive_increment',
                        dest='ADAPTIVE_INCREMENT',
                        type=float,
                        help='Specifies the value used to add to the learning factor each generation. '
                        'Float Required.')

    # Parse command line arguments using all above information.
    args, _ = parser.parse_known_args(arguments)

    # All default args in the parser are set to "None".
    cmd_args = {key: value for key, value in vars(args).items() if value is
                not None}

    # Set "None" values correctly.
    for key in sorted(cmd_args.keys()):
        # Check all specified arguments.

        if type(cmd_args[key]) == str and cmd_args[key].lower() == "none":
            cmd_args[key] = None

    if 'PARAMETERS' in cmd_args:
        load_parameters(cmd_args['PARAMETERS'])
    params.update(cmd_args)

    # Default path
    params['PATH'] = params['EXPERIMENT_NAME'] + "/" + str(params['LEARNING_FACTOR']) + "/"
