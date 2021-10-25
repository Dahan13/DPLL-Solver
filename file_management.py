import DPLL
import time
import datetime
import copy
import CNF_generator as gen

def load_conjonctive(path: str):
    """Read and get data from a file"""
    file = open(path, "r") 
    lines = file.readlines()

    # Removing all starting and ending line breaks
    while lines[0] == "\n":
        lines.remove("\n")
    while lines[-1] == "\n":
        lines.pop()

    return lines
    
def separate_conjonctives(lines):
    """Separate raw data into the different conjonctives"""
    conjonctive_list = []
    last_index = 0
    for i in range(len(lines) - 1):
        if lines[i] == "\n" and lines[i + 1] == "\n":
            conjonctive_list.append((lines[:i])[last_index:])
            last_index = i + 2
    conjonctive_list.append(lines[last_index:])
    return conjonctive_list

def convert_conjonctive(conjonctive_list):
    """Convert raw conjonctives into formalized and usable ones"""
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

def get_conjonctives(path: str):
    return convert_conjonctive(separate_conjonctives(load_conjonctive(path)))

def solutions_reconstruction(solutions):
    """Takes an array of all the litterals that are solutions"""
    index = 0
    while index < len(solutions): # We use a while loop because solutions will be incremented, meaning that it's len will change and therefore needs to be updated
        literals = solutions[index]
        increment_index = True
        for key in literals.keys():
            if literals[key][0] == None: # If a literal value was not defined, conjonctive is True with either False or True, we are reconstituting these solutions
                # Copying our litterals before deleting it from solutions, also marking index not to be incremented since we are removing an element from the list
                literals = copy.deepcopy(solutions[index])
                del solutions[index]
                increment_index = False

                # Creating and appending our corrected solutions
                first_solution = copy.deepcopy(literals)
                first_solution[key] = (True, literals[key][1])
                second_solution = literals # No need for a deepcopy this time to save complexity
                second_solution[key] = (False, literals[key][1])
                solutions.append(first_solution)
                solutions.append(second_solution)
        if increment_index:
            index += 1
    return solutions

def write_results(conjonctives):
    """Will solve a conjonctive and give all kind of infos about it"""
    number_treated = 0
    for couple in conjonctives :
        number_treated += 1
        litterals = couple[0]
        conjonctive = couple[1]
        # Getting all values
        node_numbers = 2**(len(litterals.keys())) # Total number of possibilities (= combination of litteral values)
        start_solve = time.time()
        solutions = DPLL.solve(litterals, conjonctive)
        end_solve = time.time()
        start_reconstruct = time.time()
        solutions = solutions_reconstruction(solutions)
        end_reconstruct = time.time()
        exec_time_solve = end_solve - start_solve
        exec_time_reconstruct = end_reconstruct - start_reconstruct
            
        # Starting writing log
        file_title = f"./log/sat_solver_{number_treated}_{datetime.datetime.today()}.txt"
        file_title = file_title.replace(":", "_")  # To ensure windows compatibility
        f = open(file_title, "w")
        f.write(f"Number of possibilities : {node_numbers}\n")
        f.write(f"Number of solutions found : {len(solutions)}")
        f.write(f"\n Solver execution time : {exec_time_solve}s")
        f.write(f"\n Solution reconstruction execution time : {exec_time_reconstruct}s")
        f.write(f"\n Total execution time : {exec_time_solve + exec_time_reconstruct}s\n\n")
        f.write("Solutions found :\n")
        for element in solutions :
            f.write(f"- {element}\n")
        f.close()
        


write_results([gen.generate_conjonctive(20, 20)])


