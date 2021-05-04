# Probabilistic Grammatical Evolution python3 code
## Introduction

Probabilistic Grammatical Evolution (PGE) is a new alternative to Grammatical Evolution (GE), which introduces a new genotypic representation and a new method of genotype-phenotype mapping.

The mapping is done using a PCFG, and the genotype of the individuals is a list of real values. Throughout the evolutionary process the probabilities of the PCFG are updated taking into account the productions chosen by the best individual of the current generation or the best overall.

A more in-depth explanation of the method and an analysis of its performance can be found in the article, publicly available on [arXiv](https://arxiv.org/abs/2103.08389).

The original PGE article can be referenced using the following bibtex:

```
{
    @InProceedings{10.1007/978-3-030-72812-0_13,
        author="M{\'e}gane, Jessica and Louren{\c{c}}o, Nuno and Machado, Penousal",
        editor="Hu, Ting and Louren{\c{c}}o, Nuno and Medvet, Eric",
        title="Probabilistic Grammatical Evolution",
        booktitle="Genetic Programming",
        year="2021",
        publisher="Springer International Publishing",
        address="Cham",
        pages="198--213",
        isbn="978-3-030-72812-0"
    }
}
```

## Requirements

This code needs python3.5 or a newer version. More detail on the required libraries can be found in the `requirements.txt` file.

## Execution

The folder `examples/` contains the code for some benchmark problems used in GP. To run, for example, Symbolic Regression, you can use the following command:

```
$ cd pge
$ python3 -m examples.SymbolicRegression --experiment_name test_pge/quartic --grammar grammars/regression.bnf --learning_factor 0.01
```

A folder will be automatically created with the path `test_pge/quartic/0.01/`, which will contain:
* a file `parameters.json`, which stores the values used by the algorithm;
* a file `data.txt`, in which the phenotype and the fitness of the best individual of each generation are stored
* for each run *i*, a `last_i/` folder is created, which contains a *.json* file for each generation, which stores the grammar and its probabilities in dictionary format, that was used to update the individuals of that generation, and, if the `--save_pop` flag is active, it stores the information of all the individuals of that generation.

To view for each generation the statistics during the run, you can run the code with the `--verbose` argument. It will show the phenotype and fitness of the best individual of each generation.

To see the full list of arguments that can be changed via the command line, you can run the following command:

`
$ python3 -m examples.SymbolicRegression --help
`
## Support

Any questions, comments, or suggestions should be directed to Jessica Mégane (jessicac@student.dei.uc.pt) or Nuno Lourenço (naml@dei.uc.pt).

## References

O'Neill, M. and Ryan, C. "Grammatical Evolution: Evolutionary Automatic Programming in an Arbitrary Language", Kluwer Academic Publishers, 2003.

Fenton, M., McDermott, J., Fagan, D., Forstenlechner, S., Hemberg, E., and O'Neill, M. PonyGE2: Grammatical Evolution in Python. arXiv preprint, arXiv:1703.08535, 2017.
