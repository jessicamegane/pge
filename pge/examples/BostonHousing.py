from core.utilities.protected_math import _log, _exp, _sqrt, _sin, _cos, _div, _inv, isnan, isinf
from core.parameters import params

class BostonHousing():

    def __init__(self, run=0):
        self.train_set = []
        self.test_set = []
        self.run = run
        self.invalid_fitness = 9999999
        self.read_dataset()

    def __call__(self, fenotype):
        f = "".join(fenotype)
        f = f.replace("\eb", "|")
        
        trn_error = self.get_error(f, self.train_set)
        tst_error = self.get_error(f, self.test_set)

        return trn_error, tst_error

 
    def get_error(self, fenotype, dataset):
        targets = []
        outputs = []
        fitness = 0
        size = len(self.train_set)
        for case in dataset:
            target = case[-1]
            targets.append(target)
            try:
                output = eval(fenotype, globals(), {"x": case[:-1]})
                if isnan(output):
                    return self.invalid_fitness
                elif isinf(output):
                    output = self.invalid_fitness
                outputs.append(output)
                fitness += (target - output)**2
            except (SyntaxError, ValueError, OverflowError, MemoryError, FloatingPointError):
                return self.invalid_fitness
        try:
            error = sum([(targets[i] - outputs[i])**2 for i in range(len(targets))])
        except(OverflowError):
            error = self.invalid_fitness
        return self.rrse(error,dataset)
        # return _sqrt(fitness/size)

    def rrse(self, nominator, dataset):
        outputs = [values[-1] for values in dataset]
        avg = sum(outputs) / len(outputs)

        denominator = sum([(v - avg)**2 for v in outputs])

        return _sqrt(nominator/denominator)


    def read_dataset(self):
        dataset = []
        trn_ind = []
        tst_ind = []
        with open('resources/housing.data', 'r') as dataset_file:
            for line in dataset_file:
                dataset.append([float(value.strip(" ")) for value in line.split(" ") if value != ""])

        with open('resources/housing.folds', 'r') as folds_file:
            for _ in range(self.run - 1): folds_file.readline()
            tst_ind = folds_file.readline()
            tst_ind = [int(value.strip(" ")) - 1 for value in tst_ind.split(" ") if value != ""]
            trn_ind = filter(lambda x: x not in tst_ind, range(len(dataset)))
        self.train_set = [dataset[i] for i in trn_ind]
        self.test_set = [dataset[i] for i in tst_ind]
        
if __name__ == "__main__":
    import core
    core.setup()
    eval_func = BostonHousing(params['RUN'])
    core.evolutionary_algorithm(evaluation_function=eval_func)
