import random as rd

def generate_conjonctive(n_clauses, n_literals):

    # Generating litterals
    literals = {}
    for i in range(1, n_literals + 1):
        literals[i] = None

    # Generating conjonctive
    conjonctive = []

    while len(conjonctive) != n_clauses:
        clause = []
        for j in range(1, n_literals + 1):
            literal_value = rd.randint(0, 2)
            # We take the following convention : 0 is for the literal is not in the clause, 1 it is, 2 it's negation is in the clause.
            if literal_value == 1:
                clause.append(j)
            elif literal_value == 2:
                clause.append(-j)

        if len(clause) != 0:
            conjonctive.append(clause)
    return literals, conjonctive