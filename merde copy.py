import copy
litterals_test = {
    1: (None, False),
    2: (None, False),
    3: (None, False)
}

conjonctive_test = [
    [1, 2, 3],
    [-1, 2],
    [-2, 3],
    [-3, 1],
    [-1, -2, -3]
]

def clauseIsTrue(clause, litterals):
    """Tells if a clause is true given all it's litterals values"""
    for element in clause:
        if element < 0:
            element = -element
            if not litterals[element]:
                return True
        else:
            if litterals[element]:
                return True
    return False
    
def conjonctiveIsTrue(conjonctive, litterals):
    """Tells if a conjonctive is true given all it's litterals values"""
    for clause in conjonctive:
        if not clauseIsTrue(clause, litterals):
            return False
    return True

def simplify(conjonctive, litterals):
    conjonctive = copy.deepcopy(conjonctive)
    for i in range(len(conjonctive)):
        clause = conjonctive[i]
        for element in clause:
            if abs(element) in litterals.keys() and litterals[abs(element)][0] != None:
                bool_value = ((element > 0) == (litterals[abs(element)][0])) # We found the value of the litteral, depending of the bool assigned to it and if it's a negation or not
                if bool_value: # if the litteral is True, we delete the clause he is in
                    conjonctive[i] = True # Instead of deleting the clause, we assign a special value to it because deletion will cause index issues in the for loop
                else: # If the litteral is False, we remove it from the clause
                    clause.remove(element)
                    if len(clause) == 0: # if a clause is empty, all litterals inside are false so the conjonctive is false
                        return False
    if len(conjonctive) == 0: # if the conjonctive is empty, all clauses are true so the conjonctive is true
        return True
    # Deletion of all True clauses once the loop is over
    while True in conjonctive:
        conjonctive.remove(True)
    return conjonctive
            
def forever_alone_litterals(conjonctive, litterals):
    """Assigns values to mono-litterals and checks for incompatibilites between mono-litterals"""
    for clause in conjonctive:
        if len(clause) == 1 :
            if litterals[abs(clause[0])][1] and ((clause[0] > 0) != (litterals[abs(clause[0])][0])): # si la valeur est déjà affecté à l'autre signe c mort
                return False
            litterals[abs(clause[0])] = (clause[0] > 0, True) # affect value to the corresponding litterals
    return litterals

def holy_litterals(conjonctive, litterals):
    """Assigns values to pure litterals and return all the litterals"""
    litterals_found = []
    # First we use this loop to put in our modifiable all litterals we met
    for clause in conjonctive:
        for element in clause:
            if element not in litterals_found:
                litterals_found.append(element)
    # Now we checks if there is litterals and their negation into the modifiable
    holy_litterals = []
    for element in litterals_found :
        if not(-element in litterals_found):
            litterals[abs(element)] = (element > 0, True)
    return litterals

def initialize_solving(conjonctive, litterals):
    """This will loop through the conjonctive by simplifying all mono-litterals and pure litterals"""
    litterals = forever_alone_litterals(conjonctive, litterals)
    if not(litterals):
        return False
    simplified_conjonctive = simplify(conjonctive, litterals)
    if simplified_conjonctive == True:
        return litterals,"\n",conjonctive,"The End"
    elif simplified_conjonctive == False:
        return False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        litterals = forever_alone_litterals(conjonctive, litterals)
        if not(litterals):
            return False
        simplified_conjonctive = simplify(conjonctive, litterals)
        if simplified_conjonctive == True:
            return litterals,"\n",conjonctive,"The End"
        elif simplified_conjonctive == False:
            return False

    
    litterals = holy_litterals(simplified_conjonctive, litterals)
    simplified_conjonctive = simplify(conjonctive, litterals)
    if simplified_conjonctive == True:
        return litterals,"\n",conjonctive,"The End"
    elif simplified_conjonctive == False:
        return False
    while simplified_conjonctive != conjonctive:
        conjonctive = simplified_conjonctive
        litterals = holy_litterals(simplified_conjonctive, litterals) 
        simplified_conjonctive = simplify(conjonctive, litterals)
        if simplified_conjonctive == True:
            return litterals,"\n",conjonctive,"The End"
        elif simplified_conjonctive == False:
            return False
    return litterals, simplified_conjonctive

def to_be_modified(litterals):
    modifiable = []
    modified = {}
    for i in litterals.keys():
        if not litterals[i][1]:
            modifiable.append(i)
            modified[i] = 0
    return modifiable, modified

def proceed(litterals, conjonctive, pile, modifiable_litterals, modified):
    # Case where no litterals were treated yet
    if pile == []:
        litteral = modifiable_litterals[0]
    # If at least one litteral was treated
    else:
        last_litterals = pile[-1] # previous litteral
        litteral = modifiable_litterals[modifiable_litterals.index(last_litterals) + 1] # current litteral
    # We attribute value to the litteral and update corresponding parameters
    litterals[litteral] = (True, False)
    pile.append(litteral)
    modified[litteral] += 1
    return litterals

def fail(litterals, conjonctive, pile, modifiable_litterals, modified):
    litteral = pile[-1]
    litterals[litteral] = (False, False)
    modified[litteral] += 1
    return litterals

def back(litterals, conjonctive, pile, modifiable_litterals, modified):
    # Case we went back to the beginning
    if pile == []:
        return False
    # Case at least one litteral was treated

    ### We reinitialize parameters for the litteral we are backing for
    litteral = pile[-1]
    modified[litteral] = 0
    litterals[litteral] = (None,False)
    ###
    pile.pop()
    litteral = pile[-1]
    if modified[litteral] >= 2:
        back(litterals, conjonctive, pile, modifiable_litterals, modified)
    litterals[litteral] = (False, False)
    modified[litteral] += 1
    return litterals



def solve(litterals:dict, conjonctive):
    # We begin by simplifying all mono-litterals
    original_conjonctive = copy.deepcopy(conjonctive)
    litterals, conjonctive = initialize_solving(conjonctive, litterals)
    modifiable_litterals, modified = to_be_modified(litterals)
    pile = []
    temp_litterals = copy.deepcopy(litterals)

    # Shit is about to go down:
    temp_litterals = proceed(temp_litterals, conjonctive,pile ,modifiable_litterals, modified)
    cal_12 = True
    while cal_12:

        temp_conjonctive = simplify(conjonctive, temp_litterals)
        print(conjonctive)
        if isinstance(conjonctive, bool):
            if conjonctive:
                cal_12 = False
            else:
                if temp_litterals[pile[-1]][0]:
                    temp_litterals = fail(temp_litterals, conjonctive,pile ,modifiable_litterals, modified)
                else:
                    temp_litterals = back(temp_litterals, conjonctive,pile ,modifiable_litterals, modified)
        else:
            temp_litterals = proceed(temp_litterals, conjonctive,pile ,modifiable_litterals, modified)

    return (f"litterals: {temp_litterals}\npile: {pile}\nmodifiable_litterals: {modifiable_litterals}\nmodified: {modified}")

print(solve(litterals_test, conjonctive_test))
