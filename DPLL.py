import copy


def clauseIsTrue(clause, literals):
    """Tells if a clause is true given all it's literals values"""
    for element in clause:
        if element < 0:
            element = -element
            if not literals[element]:
                return True
        else:
            if literals[element]:
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


def simplify(conjonctive, litterals, modified, pile):
    """This function simplify a conjonctive. For optimization purpose, the function works with a length vector instead of using the whole CNF"""
    length_vector = generate_length_vector(conjonctive)
    # Complexity of deepcopy : O(n²), complexity of length generation : O(n). Added to it the lessen complexity of not editing an array of array, it's quite simpler.
    for i in range(len(length_vector)):
        clause = conjonctive[i]
        for element in clause:
            if length_vector[i] == -1: # In case the clause is already satisfied, we can stop the for loop for this clause
                break

            if abs(element) in litterals.keys() and litterals[abs(element)] != None:
                bool_value = ((element > 0) == (litterals[abs(element)])) # We found the value of the litteral, depending of the bool assigned to it and if it's a negation or not
                if bool_value: # if the litteral is True, we delete the clause he is in
                    length_vector[i] = -1 # We indicate that the clause is True (we do not use True because the function may take a 1 for a True, see the last if of the function)
                else: # If the litteral is False, we remove it from the clause, meaning there is one less term in the clause
                    length_vector[i] -= 1
        if length_vector[i] == 0: # if a clause is empty (it's length is 0), all litterals inside are false so the conjonctive is false
            return False
    if length_vector.count(-1) == len(length_vector): # if all clauses are true (there is as mush satisfied clauses as there is clauses)
        return True
    
    return length_vector
    

def mono_literals(conjonctive, literals, modified, pile, length_vector):
    """Assigns values to mono-litterals and checks for incompatibilities between mono-litterals"""
    if not isinstance(length_vector, bool):
        for i in range(len(conjonctive)):
            if length_vector[i] == 1:
                index = 0
                clause = conjonctive[i]
                # Looking for the mono_literal
                for j in range(len(clause)):
                    element = clause[j]
                    if literals[abs(element)] == None: # If the element is not having any value, he is the chosen one
                        index = j
                        break
                if modified[abs(clause[index])] == 2 and ((clause[index] > 0) != (literals[abs(clause[index])])): # si la valeur est déjà affecté à l'autre signe c mort
                    return literals, False
                literals[abs(clause[index])] = (clause[index] > 0) # affect value to the corresponding literals
                modified[abs(clause[index])] = 2 # To make the program believe that the value of the literal is definitive
                pile.append(abs(clause[index]))
    return literals, True


def pure_literals(conjonctive, literals, modified, pile):
    """Assigns values to pure literals and return all the literals"""
    literals_found = []
    # First we use this loop to put in our modifiable all literals we met
    for clause in conjonctive:
        for element in clause:
            if element not in literals_found:
                literals_found.append(element)
    # Now we checks if there is literals and their negation into the modifiable
    pure_literals = []
    for element in literals_found :
        if not(-element in literals_found):
            literals[abs(element)] = (element > 0)
            modified[abs(element)] += 1
            pile.append(abs(element))
    return literals


def initialize_solving(conjonctive, literals):
    """This will loop through the conjonctive by simplifying all mono-literals and pure literals"""
    modified = [0 for i in range(len(literals.keys()) + 1)]
    modified[0] = -1
    pile = []
    length_vector = generate_length_vector(conjonctive)
    literals, status = mono_literals(conjonctive, literals, modified, pile, length_vector)
    if not(status):
        return False
    conjonctive = simplify_CNF(conjonctive, literals)
    
    return literals, conjonctive, modified, pile, length_vector

    
def first_satisfy(conjonctive, literals):
    counter = {}
    for i in range(1, len(literals) + 1):
        counter[i] = 0
    keys = counter.keys()
    for clause in conjonctive:
        for literal in clause:
            if literals[abs(literal)] == None and literal in keys:
                counter[literal] += 1
    return max(counter, key=counter.get)

def first_fail(conjonctive, literals):
    counter_neg = {}
    for i in range(-1, -(len(literals) + 1), -1):
        counter_neg[i] = 0
    keys = counter_neg.keys()
    for clause in conjonctive:
        for literal in clause:
            if literals[abs(literal)] == None and literal in keys:
                counter_neg[literal] += 1
    return -(max(counter_neg, key = counter_neg.get))


def proceed(conjonctive, literals, pile, modified, mode = 0):
    """Proceed to the next litteral withing the possibility tree"""
    literals_list = list(literals.keys())
    # Case where no literals were treated yet
    if pile == []:
        if mode == 0:
            literal = literals_list[0]
        elif mode == 1:
            literal = first_satisfy(conjonctive,literals)
        elif mode == 2:
            literal = first_fail(conjonctive,literals)

    # If at least one literal was treated
    else:
        if mode == 0:
            literal = modified.index(0)
        elif mode == 1:
            literal = first_satisfy(conjonctive,literals)
        elif mode == 2:
            literal = first_fail(conjonctive,literals)
    # We attribute value to the literal and update corresponding parameters
    literals[literal] = True
    pile.append(literal)
    modified[literal] += 1
    return literals
    

def fail(literals, pile, modified):
    literal = pile[-1]
    literals[literal] = not(literals[literal])
    modified[literal] += 1
    return literals


def back(literals, conjonctive, pile, modified):
    # Case we went back to the beginning
    if len(pile) == 1 :
        return False
    # Case at least one literal was treated

    ### We reinitialize parameters for the literal we are backing for
    literal = pile[-1]
    modified[literal] = 0
    literals[literal] = None
    ###
    pile.pop()
    literal = pile[-1]
    if modified[literal] >= 2:
        return back(literals, conjonctive, pile, modified)
    literals[literal] = not(literals[literal])
    modified[literal] += 1
    return literals



def solve(literals:dict, conjonctive, first_solution_only = False, mode = 0):
    # We begin by simplifying all mono-literals
    counter = 0
    init = initialize_solving(conjonctive,literals)
    if isinstance(init, bool):
        if not(init):
            return []
    literals, conjonctive, modified, pile, length_vector = init
    if isinstance(conjonctive, bool):
        return [literals]

    # Shit is about to go down:
    cal_12 = True
    solutions = []
    while cal_12:
        counter += 1
        #print(f"1 conjonctive : {conjonctive}\nlitteraux : {literals}\n length_vector : {length_vector}\n\n")
        length_vector = simplify(conjonctive, literals, modified, pile)
        #print(f"2 conjonctive : {conjonctive}\nlitteraux : {literals}\n length_vector : {length_vector}\n\n")
        if isinstance(length_vector, bool):
            if length_vector:
                if first_solution_only :
                    return [literals]
                solutions.append(copy.deepcopy(literals))
                if modified[pile[-1]] == 1:
                    literals = fail(literals, pile, modified)
                else:
                    literals = back(literals, conjonctive, pile, modified)
                    if literals == False: 
                        cal_12 = False
            else:
                if modified[pile[-1]] == 1:
                    literals = fail(literals, pile, modified)
                else:
                    literals = back(literals, conjonctive, pile, modified)
                    if literals == False:
                        cal_12 = False
        else:
            literals = proceed(conjonctive, literals, pile, modified, mode)

    
    #return (f"literals: {literals}\npile: {pile}\nmodifiable_literals: {modifiable_literals}\nmodified: {modified}")
    return solutions, counter
    

def naive_solve(literals, conjonctive):
    literals = copy.deepcopy(literals)
    """This solver will naively try all combinations of literals to see which ones are functioning"""
    solutions = []
    literals_binary = [0 for i in range(len(literals))]
    final = [1 for i in range(len(literals))]
    for i in range(len(literals_binary)):
        literals[i + 1] = bool(literals_binary[i])
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
            literals[i + 1] = bool(literals_binary[i])
        if conjonctiveIsTrue(conjonctive, literals):
            solutions.append(copy.deepcopy(literals))
    return solutions


############################################################ DEAD ZONE ############################################################

def simplify_CNF(conjonctive, literals):
    """This function simplify a conjonctive BY REMOVING ELEMENTS IN IT. Use with caution"""
    temp_conjonctive = copy.deepcopy(conjonctive)
    for i in range(len(temp_conjonctive)):
        clause = temp_conjonctive[i]
        for element in clause:
            if abs(element) in literals.keys() and literals[abs(element)] != None:
                bool_value = ((element > 0) == (literals[abs(element)])) # We found the value of the literal, depending of the bool assigned to it and if it's a negation or not
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


def old_initialize_solving(conjonctive, literals):
    """This will loop through the conjonctive by simplifying all mono-literals and pure literals"""
    literals = mono_literals(conjonctive, literals)
    if not(literals):
        return False, False
    simplified_conjonctive = simplify(conjonctive, literals)
    if simplified_conjonctive == True:
        return True, literals
    elif simplified_conjonctive == False:
        return False, False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        literals = mono_literals(conjonctive, literals)
        if not(literals):
            return False, False
        simplified_conjonctive = simplify(conjonctive, literals)
        if simplified_conjonctive == True:
            return True, literals
        elif simplified_conjonctive == False:
            return False, False

    
    literals = pure_literals(simplified_conjonctive, literals)
    simplified_conjonctive = simplify(conjonctive, literals)
    if simplified_conjonctive == True:
        return True, literals
    elif simplified_conjonctive == False:
        return False, False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        literals = pure_literals(simplified_conjonctive, literals) 
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
        if not literals[i]:
            modifiable.append(i)
            modified[i] = 0
    return modifiable, modified