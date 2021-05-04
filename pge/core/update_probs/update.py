import core.grammar as grammar

def update_probs(best, lf):
    """ Function to update the probabilities of the PCFG,
    based on the productions chosen to construct the selected individual.
    """
    gram_counter = best['gram_counter']
    for key, val in gram_counter.items():
        total = sum(val)
        if total > 0:
            l = [0] * len(val)
            for pos in range(len(val)):
                counter = val[pos]
                old_prob = grammar.get_dict()[key][pos][1]
                prob_updated = old_prob
                if counter > 0:
                    prob_updated = round(min(old_prob + lf * counter / total, 1.0),14)
                elif counter == 0:
                    prob_updated = round(max(old_prob - lf * prob_updated, 0.0),14)

                l[pos] = prob_updated

            # Adjust probabilities - divide the remaining equally by all productions
            while(round(sum(l),3) != 1.0):
                if sum(l) > 1.0:
                    res = sum(l) - 1.0
                    diff = res / len(l)
                    for i in range(len(l)):
                        new = round(l[i] - diff,14)
                        l[i] = max(new,0.0)
                elif sum(l) < 1.0 and sum(l) > 0.0:
                    res = 1.0 - sum(l)
                    diff = res / len(l)
                    for i in range(len(l)):
                        new = round(l[i] + diff,14)
                        l[i] = min(diff,1.0)

            for i in range(len(l)):
                grammar.get_dict()[key][i][1] = l[i]

    print("Probabilities updated")
    print(grammar.get_dict())
