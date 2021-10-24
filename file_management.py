def load_conjonctive(path: str):
    file = open(path, "r") 
    lines = file.readlines()

    # Removing all starting and ending line breaks
    while lines[0] == "\n":
        lines.remove("\n")
    while lines[-1] == "\n":
        lines.pop()

    return lines
    
def separate_conjonctives(lines):
    conjonctive_list = []
    for i in range(len(lines) - 1):
        if lines[i] == "\n" and lines[i + 1] == "\n":
            conjonctive_list.append(lines[:i])
            last_index = i + 2
    conjonctive_list.append(lines[last_index:])
    return conjonctive_list

def convert_conjonctive(conjonctive_list):
    conjonctives = []
    for raw_conjonctive in conjonctive_list:

        # Generating dictionary of litterals :
        litterals = {}
        litteral_number = int(raw_conjonctive[0][:len(raw_conjonctive[0]) - 1])
        for i in range(1, litteral_number + 1):
            litterals[i] = (None, False)

        # Generating the conjonctive
        raw_clauses = raw_conjonctive[2:]
        conjonctive = []
        for raw_clause in raw_clauses:
            if '\n' in raw_clause: # Deleting line break 
                raw_clause = raw_clause[:len(raw_clause)-1]
            terms = raw_clause.split(' ')
            clause = [int(terms[i]) for i in range(len(terms))]
            conjonctive.append(clause)
        conjonctives.append((litterals, conjonctive))
    return conjonctives



conjonctives = convert_conjonctive(separate_conjonctives(load_conjonctive("./load.txt")))
for element in conjonctives:
    print(element[0])
    print(element[1])
    print('\n\n')