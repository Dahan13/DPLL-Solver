import random as rd

def generate_conjonctive(n_literals, n_clauses, saving = True):

    # Generating literals
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
    if saving:
        name = input("Enter the name to save the generated conjonctive :\n")
        save_conjonctive(name, literals, conjonctive)
    return literals, conjonctive

def generate_pigeon(n, saving = True):
    """Trying to put n pigeons in n - 1 houses with 1 pigeon per house"""
    # Generating literals
    bijection = {}
    literals = {}
    for i in range(1, n+1): # i represent the pigeon
        for j in range(1, n): # j represent the house
            bijection[(i,j)] = None
    for i in range(1, len(bijection) + 1):
        literals[i] = None
    # Generating clauses
    conjonctive = []
    literals_keys = list(literals.keys())
    bijection_keys = list(bijection.keys())
    for i in range(1, n + 1):
        conjonctive.append([literals_keys[bijection_keys.index((i, m))] for m in range(1, n)])
        for j in range(1, n + 1):
            for k in range(1, n):
                if i != j:
                    conjonctive.append([-literals_keys[bijection_keys.index((i, k))], -literals_keys[bijection_keys.index((j, k))]])
                    for l in range(1, n):
                        if k != l:
                            conjonctive.append([-literals_keys[bijection_keys.index((i, k))], -literals_keys[bijection_keys.index((i, l))]])
    # Now removing doubles from the list
    conjonctive_keep = []
    for element in conjonctive:
        element.sort() # Because doubles may comes but ordered differently
        if not(element in conjonctive_keep):
            conjonctive_keep.append(element)
    # Saving and returning
    if saving:
        name = input("Enter the name to save the generated conjonctive :\n")
        save_conjonctive(name, literals, conjonctive_keep)
    return literals, conjonctive

def generate_queens(n,saving = True):
    """Simp function that generate a N-queens problem"""
    # Generating literals
    bijection = {}
    literals = {}
    for i in range(1, n + 1): # i represents the line
        for j in range(1, n + 1): # j represents the column
            bijection[(i,j)] = None
    for i in range(1, len(bijection) + 1):
        literals[i] = None
    # Generating clauses for lines
    conjonctive = []
    literals_keys = list(literals.keys())
    bijection_keys = list(bijection.keys())
    for i in range(1, n + 1):
        conjonctive.append([literals_keys[bijection_keys.index((m, i))] for m in range(1, n + 1)])
        for j in range(1, n + 1):
            # Generating clauses related to diagonals. 
            if i != n: # Condition to have an actual diagonal below
                for m in range(1, n):
                    if  i + m <= n and j + m <= n: # (i + m, j + m) are coordinates of an element of the diagonal
                        conjonctive.append([-literals_keys[bijection_keys.index((i, j))], -literals_keys[bijection_keys.index((i + m, j + m))]])
                    if i + m <= n and 1 <= j - m: # (i + m, j - m) are coordinates of an element of the anti-diagonal
                        conjonctive.append([-literals_keys[bijection_keys.index((i, j))], -literals_keys[bijection_keys.index((i + m, j - m))]])
            for k in range(1, n + 1):
                if j != k:
                    conjonctive.append([-literals_keys[bijection_keys.index((i, j))], -literals_keys[bijection_keys.index((i, k))]])
                    conjonctive.append([-literals_keys[bijection_keys.index((j, i))], -literals_keys[bijection_keys.index((k, i))]]) # ! The clauses this line create are useless but somehow it makes the solving faster
    # Now removing doubles from the list
    conjonctive_keep = []
    for element in conjonctive:
        element.sort() # Because doubles may comes but ordered differently
        if not(element in conjonctive_keep):
            conjonctive_keep.append(element)
    # Saving and returning
    if saving:
        name = input("Enter the name to save the generated conjonctive :\n")
        save_conjonctive(name, literals, conjonctive_keep)
    return literals, conjonctive_keep

def save_conjonctive(name, literals, conjonctive):
    path = f"./saves/{name}"
    path += ".txt"
    f= open(path, "w")
    f.write(f"{len(literals)}\n\n")
    for clause in conjonctive:
        for literal in clause:
            f.write(f"{literal} ")
        f.write("\n")
    print(f"Conjonctive saved at : \"{f.name}\"")
    f.close()