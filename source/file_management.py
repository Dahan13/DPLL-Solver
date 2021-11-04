from typing import Literal
from source import DPLL
import time
import datetime
import copy

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
            litterals[i] = None

        # Generating the conjonctive
        raw_clauses = raw_conjonctive[2:]
        conjonctive = []
        for raw_clause in raw_clauses:
            if '\n' in raw_clause: # Deleting line break 
                raw_clause = raw_clause[:len(raw_clause)-1]
            terms = raw_clause.split(' ')
            while '' in terms:
                terms.remove('')
            clause = [int(terms[i]) for i in range(len(terms))]
            conjonctive.append(clause)
        conjonctives.append((litterals, conjonctive))
    print("Converted")
    return conjonctives

def get_conjonctives(path: str):
    print("Initialise loading")
    return convert_conjonctive(separate_conjonctives(load_conjonctive(path)))
    print("Ready to work")

def solutions_reconstruction(solutions):
    """Takes an array of all the litterals that are solutions"""
    index = 0
    while index < len(solutions): # We use a while loop because solutions will be incremented, meaning that it's len will change and therefore needs to be updated
        literals = solutions[index]
        increment_index = True
        for key in literals.keys():
            if literals[key] == None: # If a literal value was not defined, conjonctive is True with either False or True, we are reconstituting these solutions
                # Copying our litterals before deleting it from solutions, also marking index not to be incremented since we are removing an element from the list
                literals = copy.deepcopy(solutions[index])
                del solutions[index]
                increment_index = False

                # Creating and appending our corrected solutions
                first_solution = copy.deepcopy(literals)
                first_solution[key] = True
                second_solution = literals # No need for a deepcopy this time to save complexity
                second_solution[key] = False
                solutions.append(first_solution)
                solutions.append(second_solution)
                break
        if increment_index:
            index += 1
    return solutions

def write_results(conjonctives, only_one_solution = False, show_naive = True, mode = 0):
    """Will solve a conjonctive and give all kind of infos about it"""
    number_treated = 0
    for couple in conjonctives :
        number_treated += 1
        litterals = couple[0]
        conjonctive = couple[1]
        # Getting all values
        node_numbers = 2**(len(litterals.keys())) # Total number of possibilities (= combination of litteral values)
        print("\n\n/!\\ Starting calculation /!\\")
        start_solve = time.time()
        solutions, counter = DPLL.solve(litterals, conjonctive, only_one_solution, mode)
        end_solve = time.time()
        
        if only_one_solution:
            solutions = [solutions[0]]
        
        exec_time_solve = end_solve - start_solve
        if show_naive and not(only_one_solution):
            print("Starting reconstruction")
            start_reconstruct = time.time()
            solutions = solutions_reconstruction(solutions)
            end_reconstruct = time.time()
            exec_time_reconstruct = end_reconstruct - start_reconstruct
            print("Starting naive calculation")
            start_naive = time.time()
            naive_solution = DPLL.naive_solve(litterals, conjonctive)
            end_naive = time.time()
            exec_time_naive = end_naive - start_naive
            solution_checker = True
            if len(solutions) != len(naive_solution) or len(solutions) > node_numbers: # Testing some worst case scenarios
                print("A critical error occurred")
            for solution in naive_solution:
                if solution not in solutions:
                    solution_checker = False
                    break
        
        print("Creating log")
        if mode == 0:
            heuristic_name = "Naive"
        elif mode == 1:
            heuristic_name = "First satisfy"
        elif mode == 2:
            heuristic_name = "First fail"
            
        # Starting writing log
        file_title = f"./log/sat_solver_{number_treated}_{datetime.datetime.today()}.txt"
        file_title = file_title.replace(":", "_")  # To ensure windows compatibility
        f = open(file_title, "w")
        f.write(f"Number of possibilities : {node_numbers}\n")
        f.write(f"Number of solutions found : {len(solutions)}\n")
        f.write(f"Number of nodes traveled : {counter}\n")
        f.write(f"Heuristic chosen : {heuristic_name}\n")
        f.write(f"Solver execution time : {exec_time_solve}s\n")
        f.write(f"Conjonctive treated : {conjonctive}\n\n")
        if show_naive and not(only_one_solution):
            f.write(f"Solution reconstruction execution time : {exec_time_reconstruct}s\n")
            f.write(f"Naive solver execution time : {exec_time_naive}s\n")
            f.write(f"Result comparison with naive solver : {solution_checker}\n")
            
        if len(solutions) != 0:
            f.write("Solutions found :\n")
            for element in solutions :
                f.write(f"- {element}\n")
        else:
            f.write("No solutions found\n")
        
        if show_naive and not(only_one_solution):
            if len(naive_solution) != 0:
                f.write("\n\nNaive solutions found :\n")
                for element in naive_solution :
                    f.write(f"- {element}\n")
            else:
                f.write("Naive solver found no solutions")
        print(f"Log saved at : \"{f.name}\"")
        f.close()
