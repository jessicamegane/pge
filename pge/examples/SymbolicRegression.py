from core.utilities.protected_math import _log, _exp, _sqrt, _sin, _cos, _div, _inv, isnan, isinf
import numpy as np

def quartic_polynomial():
    l = []
    for inp in np.arange(-1,1.1,0.1):
        out = pow(inp,4) + pow(inp,3) + pow(inp,2) + inp
        l.append([inp,out])
    return l

def pagie_polynomial():
    l = []
    for inp1 in np.arange(-5,5.4,0.4):
        for inp2 in np.arange(-5,5.4,0.4):
            out = 1.0 / (1 + pow(inp1,-4.0)) + 1.0 / (1 + pow(inp2,-4.0))
            l.append([inp1,inp2,out])
    return l

def keijzer6_polynomial(xx):
    l = []
    for inp in xx:
        out = sum([1.0/i for i in range(1,inp+1,1)])
        l.append([inp,out])
    return l

def keijzer9_polynomial(xx):
    l = []
    for inp in xx:
        out = _log_(inp + (inp**2 + 1)**0.5)
        l.append([inp,out])
    return l

class SymbolicRegression():

    def __init__(self, polynomial = "quartic"):
        self.polynomial = polynomial
        self.test_set = None
        self.invalid_fitness = 9999999
        if self.polynomial == "pagie":
            self.train_set = pagie_polynomial()
        elif self.polynomial == "quartic":
            self.train_set = quartic_polynomial()
        elif self.polynomial == "keijzer6":
            self.train_set = keijzer6_polynomial(np.arange(1,51,1))
            self.test_set = keijzer6_polynomial(np.arange(51,121,1))
        elif self.polynomial == "keijzer9":
            self.train_set = keijzer9_polynomial(np.arange(0,101,1))
            self.test_set = keijzer9_polynomial(np.arange(0,101,0.1))
        self.calculate_rrse_denominators()


    def calculate_rrse_denominators(self):
        self.__RRSE_train_denominator = 0
        self.__RRSE_test_denominator = 0
        train_outputs = [entry[-1] for entry in self.train_set]
        train_output_mean = float(sum(train_outputs)) / len(train_outputs)
        self.__RRSE_train_denominator = sum([(i - train_output_mean)**2 for i in train_outputs])
        if self.test_set:
            test_outputs = [entry[-1] for entry in self.test_set]
            test_output_mean = float(sum(test_outputs)) / len(test_outputs)
            self.__RRSE_test_denominator = sum([(i - test_output_mean)**2 for i in test_outputs])


    def get_error(self, individual, dataset):
        pred_error = 0
        for fit_case in dataset:
            case_output = fit_case[-1]
            try:
                result = eval(individual, globals(), {"x": fit_case[:-1]})
                pred_error += (case_output - result)**2
            except (SyntaxError, ValueError, OverflowError, MemoryError, FloatingPointError) as e:
                return self.invalid_fitness
        return pred_error

    def __call__(self, individual):
        individual = individual.replace("\eb", "|")
        error = 0.0
        test_error = -1.0
        if individual is None:
            return None

        error = self.get_error(individual, self.train_set)
        error = _sqrt( error /self.__RRSE_train_denominator)

        if error is None:
            error = self.invalid_fitness

        if self.test_set is not None:
            test_error = 0
            test_error = self.get_error(individual, self.test_set)
            test_error = _sqrt( test_error / float(self.__RRSE_test_denominator))

        return error, test_error

if __name__ == "__main__":
    import core
    eval_func = SymbolicRegression("pagie")
    core.evolutionary_algorithm(evaluation_function=eval_func)
