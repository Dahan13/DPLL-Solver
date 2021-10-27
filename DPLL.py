import copy
literals_test = {
    1: (None, False),
    2: (None, False),
    3: (None, False),
    4: (None, False)
}

conjonctive_test = [
    [1, 2, 3, 4]
]

def clauseIsTrue(clause, literals):
    """Tells if a clause is true given all it's literals values"""
    for element in clause:
        if element < 0:
            element = -element
            if not literals[element][0]:
                return True
        else:
            if literals[element][0]:
                return True
    return False
    
def conjonctiveIsTrue(conjonctive, literals):
    """Tells if a conjonctive is true given all it's literals values"""
    for clause in conjonctive:
        if not clauseIsTrue(clause, literals):
            return False
    return True

def generate_length_vector(conjonctive):
    """This function will generate the length vector corresponding to the given conjonctive"""
    return [len(conjonctive[i]) for i in range(len(conjonctive))]

def simplify_CNF(conjonctive, literals):
    """This function simplify a conjonctive BY REMOVING ELEMENTS IN IT. Use with caution"""
    temp_conjonctive = copy.deepcopy(conjonctive)
    for i in range(len(temp_conjonctive)):
        clause = temp_conjonctive[i]
        for element in clause:
            if abs(element) in literals.keys() and literals[abs(element)][0] != None:
                bool_value = ((element > 0) == (literals[abs(element)][0])) # We found the value of the literal, depending of the bool assigned to it and if it's a negation or not
                if bool_value: # if the literal is True, we delete the clause he is in
                    temp_conjonctive[i] = True # Instead of deleting the clause, we assign a special value to it because deletion will cause index issues in the for loop
                else: # If the literal is False, we remove it from the clause
                    clause[clause.index(element)] = False
        while False in clause:
            clause.remove(False)
        if len(clause) == 0: # if a clause is empty, all literals inside are false so the conjonctive is false
            return False
    # Deletion of all True clauses once the loop is over
    while True in temp_conjonctive:
        temp_conjonctive.remove(True)
    if len(temp_conjonctive) == 0: # if the conjonctive is empty, all clauses are true so the conjonctive is true
        return True
    return temp_conjonctive

def simplify(conjonctive, litterals):
    """This function simplify a conjonctive. For optimization purpose, the function works with a length vector instead of using the whole CNF"""
    length_vector = generate_length_vector(conjonctive) # Complexity of deepcopy : O(n²), complexity of length generation : O(n). Added to it the lessen complexity of not editing an array of array, it's quite simpler.
    for i in range(len(conjonctive)):
        clause = conjonctive[i]
        for element in clause:
            if length_vector[i] == -1: # In case the clause is already satisfied, we can stop the for loop for this clause
                break

            if abs(element) in litterals.keys() and litterals[abs(element)][0] != None:
                bool_value = ((element > 0) == (litterals[abs(element)][0])) # We found the value of the litteral, depending of the bool assigned to it and if it's a negation or not
                if bool_value: # if the litteral is True, we delete the clause he is in
                    length_vector[i] = -1 # We indicate that the clause is True (we do not use True because the function may take a 1 for a True, see the last if of the function)
                else: # If the litteral is False, we remove it from the clause, meaning there is one less term in the clause
                    length_vector[i] -= 1
        if length_vector[i] == 0: # if a clause is empty (it's length is 0), all litterals inside are false so the conjonctive is false
            return False
    if length_vector.count(-1) == len(length_vector): # if all clauses are true (there is as mush satisfied clauses as there is clauses)
        return True
    return conjonctive

def forever_alone_literals(conjonctive, literals):
    """Assigns values to mono-litterals and checks for incompatibilities between mono-litterals"""
    for clause in conjonctive:
        if len(clause) == 1 :
            if literals[abs(clause[0])][1] and ((clause[0] > 0) != (literals[abs(clause[0])][0])): # si la valeur est déjà affecté à l'autre signe c mort
                return False
            literals[abs(clause[0])] = (clause[0] > 0, True) # affect value to the corresponding literals
    return literals

def holy_literals(conjonctive, literals):
    """Assigns values to pure literals and return all the literals"""
    literals_found = []
    # First we use this loop to put in our modifiable all literals we met
    for clause in conjonctive:
        for element in clause:
            if element not in literals_found:
                literals_found.append(element)
    # Now we checks if there is literals and their negation into the modifiable
    holy_literals = []
    for element in literals_found :
        if not(-element in literals_found):
            literals[abs(element)] = (element > 0, True)
    return literals


def initialize_solving(conjonctive, literals):
    """This will loop through the conjonctive by simplifying all mono-literals and pure literals"""
    literals = forever_alone_literals(conjonctive, literals)
    if not(literals):
        return False, False
    simplified_conjonctive = simplify(conjonctive, literals)
    if simplified_conjonctive == True:
        return True, literals
    elif simplified_conjonctive == False:
        return False, False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        literals = forever_alone_literals(conjonctive, literals)
        if not(literals):
            return False, False
        simplified_conjonctive = simplify(conjonctive, literals)
        if simplified_conjonctive == True:
            return True, literals
        elif simplified_conjonctive == False:
            return False, False

    
    literals = holy_literals(simplified_conjonctive, literals)
    simplified_conjonctive = simplify(conjonctive, literals)
    if simplified_conjonctive == True:
        return True, literals
    elif simplified_conjonctive == False:
        return False, False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        literals = holy_literals(simplified_conjonctive, literals) 
        simplified_conjonctive = simplify(conjonctive, literals)
        if simplified_conjonctive == True:
            return True, literals
        elif simplified_conjonctive == False:
            return False, False
    return literals, simplified_conjonctive

def to_be_modified(literals):
    modifiable = []
    modified = {}
    for i in literals.keys():
        if not literals[i][1]:
            modifiable.append(i)
            modified[i] = 0
    return modifiable, modified

def proceed(literals, conjonctive, pile, modifiable_literals, modified):
    """Proceed to the next litteral withing the possibility tree"""
    # Case where no literals were treated yet
    if pile == []:
        literal = modifiable_literals[0]
    # If at least one literal was treated
    else:
        last_literals = pile[-1] # previous literal
        literal = modifiable_literals[modifiable_literals.index(last_literals) + 1] # current literal
    # We attribute value to the literal and update corresponding parameters
    literals[literal] = (True, False)
    pile.append(literal)
    modified[literal] += 1
    return literals

def fail(literals, conjonctive, pile, modifiable_literals, modified):
    literal = pile[-1]
    literals[literal] = (False, False)
    modified[literal] += 1
    return literals

def back(literals, conjonctive, pile, modifiable_literals, modified):
    # Case we went back to the beginning
    if len(pile) == 1 :
        return False
    # Case at least one literal was treated

    ### We reinitialize parameters for the literal we are backing for
    literal = pile[-1]
    modified[literal] = 0
    literals[literal] = (None,False)
    ###
    pile.pop()
    literal = pile[-1]
    if modified[literal] >= 2:
        return back(literals, conjonctive, pile, modifiable_literals, modified)
    literals[literal] = (False, False)
    modified[literal] += 1
    return literals



def solve(literals:dict, conjonctive, first_solution_only = False):
    # We begin by simplifying all mono-literals
    """
    init = initialize_solving(conjonctive, literals)
    if isinstance(init[0], bool):
        return [init[1]]
    else:
        literals, conjonctive = init
    """
    modifiable_literals, modified = to_be_modified(literals)
    pile = []
    conjonctive_save = copy.deepcopy(conjonctive)
    temp_literals = copy.deepcopy(literals)

    # Shit is about to go down:
    temp_literals = proceed(temp_literals, conjonctive,pile ,modifiable_literals, modified)
    cal_12 = True
    solutions = []
    while cal_12:
        #print(f"A conjonctive : {conjonctive}\nlitteraux : {temp_literals}\n\n")
        conjonctive = simplify(conjonctive_save, temp_literals)
        if isinstance(conjonctive, bool):
            if conjonctive:
                if first_solution_only :
                    return [temp_literals]
                solutions.append(copy.deepcopy(temp_literals))
                if temp_literals[pile[-1]][0]:
                    temp_literals = fail(temp_literals, conjonctive,pile ,modifiable_literals, modified)
                else:
                    temp_literals = back(temp_literals, conjonctive,pile ,modifiable_literals, modified)
                    if temp_literals == False:
                        cal_12 = False
            else:
                if temp_literals[pile[-1]][0]:
                    temp_literals = fail(temp_literals, conjonctive,pile ,modifiable_literals, modified)
                else:
                    temp_literals = back(temp_literals, conjonctive,pile ,modifiable_literals, modified)
                    if temp_literals == False:
                        cal_12 = False
        else:
            temp_literals = proceed(temp_literals, conjonctive,pile ,modifiable_literals, modified)

    
    #return (f"literals: {temp_literals}\npile: {pile}\nmodifiable_literals: {modifiable_literals}\nmodified: {modified}")
    return solutions

def naive_solve(literals, conjonctive):
    literals = copy.deepcopy(literals)
    """This solver will naively try all combinations of literals to see which ones are functioning"""
    solutions = []
    literals_binary = [0 for i in range(len(literals))]
    final = [1 for i in range(len(literals))]
    for i in range(len(literals_binary)):
        literals[i + 1] = (bool(literals_binary[i]), literals[i + 1][1])
    if conjonctiveIsTrue(conjonctive, literals):
        solutions.append(copy.deepcopy(literals))
    while literals_binary != final:
        # Literally counting in binary to find all existing combinations
        index = -1
        while literals_binary[index] == 1:
            literals_binary[index] = 0
            index -= 1
        literals_binary[index] = 1
        # Testing if current combination may work 
        for i in range(len(literals_binary)):
            literals[i + 1] = (bool(literals_binary[i]), literals[i + 1][1])
        if conjonctiveIsTrue(conjonctive, literals):
            solutions.append(copy.deepcopy(literals))
    return solutions

