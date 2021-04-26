import os
import json

def save_state(run, gen, population, best, gram, params):
    """ Function that saves the grammar and population of the current generation and run. """
    to_save = []
    to_save.append({"grammar": gram.get_rules()})

    if params['SAVE_POP']:
        for index, ind in enumerate(population):
            to_save.append({"genotype": ind['genotype'],
                "fenotype": ind['phenotype'],
                "fitness": ind['fitness'],
                "id": index
            })
    folder = params['PATH'] + 'last_' + str(run)
    if not os.path.exists(folder):
        os.makedirs(folder,  exist_ok=True)
    open('%s/generation_%d.json' % (folder,(gen)), 'w').write(json.dumps(to_save))

    # save info of best individual overall
    f = open(params['PATH'] + "data.txt","a")
    s = '\n%d,%s,%f,%f' %(gen,"".join(best['phenotype']), best['fitness'], best['tst_error'])
    f.write(s)
    f.close()

def save_parameters(params):
    folder = params['PATH']
    params_lower = dict((k.lower(), v) for k, v in params.items())
    c = json.dumps(params_lower)
    if not os.path.exists(folder):
        os.makedirs(folder,  exist_ok=True)
    open('%sparameters.json' % (folder), 'a').write(c)

