"""
Code adapted from https://github.com/nunolourenco/dsge/blob/master/src/examples/parity_5.py 
Lots of code taken from deap
"""
input_names = ['b0', 'b1', 'b2', 'b3', 'b4']

PARITY_FANIN_M = 5
PARITY_SIZE_M = 2**PARITY_FANIN_M

inputs = [None] * PARITY_SIZE_M
outputs = [None] * PARITY_SIZE_M

for i in range(PARITY_SIZE_M):
    inputs[i] = [None] * PARITY_FANIN_M
    value = i
    dividor = PARITY_SIZE_M
    parity = 1
    for j in range(PARITY_FANIN_M):
        dividor /= 2
        if value >= dividor:
            inputs[i][j] = 1
            parity = int(not parity)
            value -= dividor
        else:
            inputs[i][j] = 0
    outputs[i] = parity

class Parity5():
    
    def __init__(self):
        self.invalid_fitness = 1000

    def __call__(self, phenotype):
        error = PARITY_SIZE_M
        for i, inpt in enumerate(inputs):
            try:
                res = eval(phenotype, dict(zip(input_names, inpt)))
            except(SyntaxError, ValueError, OverflowError, MemoryError, RuntimeWarning):
                return self.invalid_fitness, -1

            if res == outputs[i]:
                error -= 1
        return error, -1

if __name__ == "__main__":
    import core
    eval_func = Parity5()
    core.evolutionary_algorithm(evaluation_function=eval_func)