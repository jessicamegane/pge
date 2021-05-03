from core.parameters import params
import json
import os

def evolution_progress(gen, population, best, gram):
    """ Function that saves the grammar and population of the current generation and run. """
    data = '%d,%s,%f,%f' %(gen,"".join(best['phenotype']), best['fitness'], best['tst_error'])
    if params['VERBOSE']:
        print(data)
    save_progress_to_file(data)

    to_save = []
    to_save.append({"grammar": gram.get_dict})

    if params['SAVE_POP']:
        for index, ind in enumerate(population):
            to_save.append({"genotype": ind['genotype'],
                "fenotype": ind['phenotype'],
                "fitness": ind['fitness'],
                "id": index
            })
    folder = params['PATH'] + 'last_' + str(params['RUN'])
    if not os.path.exists(folder):
        os.makedirs(folder,  exist_ok=True)
    with open('%s/generation_%d.json' % (folder,(gen)), 'w') as f:
        f.write(json.dumps(to_save))

def save_progress_to_file(data):
    # save info of best individual overall
    with open(params['PATH'] + "data.txt", "a") as f:
        f.write(data + '\n')
        f.close()
    
def save_parameters():
    folder = params['PATH']
    params_lower = dict((k.lower(), v) for k, v in params.items())
    c = json.dumps(params_lower)
    if not os.path.exists(folder):
        os.makedirs(folder,  exist_ok=True)
    open('%sparameters.json' % (folder), 'a').write(c)

