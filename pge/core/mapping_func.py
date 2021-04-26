
def probabilistic_mapping(codon, productions):
    """ Probabilistic mapping, using a PCFG."""
    idx_selected_rule = len(productions) - 1
    prob_aux = 0.0
    for i in range(len(productions)):
        prob_aux += productions[i][1]
        if codon < prob_aux:
            idx_selected_rule = i
            break
    return idx_selected_rule

def mod_mapping(codon, productions):
    """ Default mapping function introduced by GE."""
    return codon%len(productions)