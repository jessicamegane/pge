"""
    Code adapted from ponyge
    https://github.com/jmmcd/ponyge

    PonyGE is copyright (C) 2009-2012 Erik Hemberg
    <erik.hemberg@gmail.com> and James McDermott
    <jamesmichaelmcdermott@gmail.com>.
"""
class StringMatch():
    """Fitness function for matching a string. Takes a string and
    returns fitness. Penalises output that is not the same length as
    the target. Usage: StringMatch("golden") returns a *callable
    object*, ie the fitness function."""
    # maximise = False
    def __init__(self, target = "pge"):
        self.target = target
        self.invalid_fitness = 100000
    
    def __call__(self, phenotype):
        fitness = max(len(self.target), len(phenotype))
        # Loops as long as the shorter of two strings
        for (t_p, g_p) in zip(self.target, phenotype):
            if t_p == g_p:
                fitness -= 1
            else:
                # Imperfect match, find ASCII distance to match.
                fitness -= 1 / (1 + (abs(ord(t_p) - ord(g_p))))
        return fitness, -1

if __name__ == "__main__":
    import core
    eval_func = StringMatch()
    core.evolutionary_algorithm(evaluation_function=eval_func)