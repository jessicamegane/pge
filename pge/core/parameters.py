import argparse
import yaml

'''
This was adapted from PonyGE2: https://github.com/PonyGE/PonyGE2
Fenton, M., McDermott, J., Fagan, D., Forstenlechner, S., Hemberg, E., and O'Neill, M. PonyGE2: Grammatical Evolution in Python. arXiv preprint, arXiv:1703.08535, 2017.
'''
""""Algorithm Parameters"""

params = {
    'PARAMETERS': None,
    'RUNS': 100,
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
    'SEED': [3601294368, 683917412, 1208919537, 1629436337, 779238096, 1216155998, 2120024179, 3600272074, 4118287191, 1643356525, 4182889281, 3445083937, 1754613280, 1796245274, 2904271034, 3559738049, 217686711, 2861030558, 1856221505, 2160446191, 1460319434, 2416604709, 414233177, 2455725808, 172153083, 1962782296, 1521279429, 1310373479, 2712692902, 483329035, 2136154935, 3438578686, 753034365, 2658976914, 2099755184, 2929949036, 1514157584, 4175105131, 2296189102, 3001892942, 4139565975, 3757821927, 2199370766, 3860104825, 3606446036, 621881453, 2259910564, 637838440, 2982145899, 3109143177, 1766549078, 3494545088, 2145142373, 2778536845, 3109498599, 2277365504, 3263755390, 1060454835, 2080946751, 3588923449, 3413853300, 76283520, 4141018352, 2687604514, 4151384417, 1226802906, 2262027499, 3611200668, 3359491764, 2993036265, 3787535003, 2594364338, 3994759752, 2226759277, 1745549554, 1135571392, 351970797, 1149575263, 3015833588, 3897076572, 1902906504, 3912057669, 719709811, 3206422566, 428652420, 1980847085, 7635194, 1215042922, 2860114456, 2492014276, 50381524, 1687357544, 2710108764, 3050496680, 3872811391, 493041932, 4111739992, 357383762, 3690204815, 320855900, 4275271226, 4162543099, 1457821592, 3515232544, 4291402216, 1122466389, 1133613368, 2305992327, 3851370364, 2920261440, 169351948, 922416999, 2807858178, 892305971, 3754505678, 116153832, 4013333916, 2862773950, 4268192256, 2319884303],
    'SAVE_POP': False,
    'PROBLEM': '5bitparity',
    'GRAMMAR': 'core/grammars/5bitparity.bnf',
    'EXPERIMENT_NAME': 'test_pge',
    'PATH': 'testes/ge/pagie/',
    'VERBOSE': False
}


def load_parameters(sle_name=None):
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
                        type=list,
                        help='Specifies the seeds to be used by the random number generator.'
                              ' One for each run.')
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
    parser.add_argument('--problem',
                        dest='PROBLEM',
                        type=str,
                        help='Specifies the name of the problem.')
    parser.add_argument('--runs',
                        dest='RUNS',
                        type=int,
                        help='Specifies the number of experiments.')
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
                        help='Specifies if it is supposed to run the adaptive version of PSGE.')
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
    params['PATH'] = params['EXPERIMENT_NAME'] + "/" + params['PROBLEM'] + "/" + str(params['LEARNING_FACTOR']) + "/"