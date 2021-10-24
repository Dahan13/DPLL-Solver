import DPLL
import time
import datetime

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
    for i in range(len(lines) - 1):
        if lines[i] == "\n" and lines[i + 1] == "\n":
            conjonctive_list.append(lines[:i])
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

def write_results(conjonctives):
    """Will solve a conjonctive and give all kind of infos about it"""
    number_treated = 0
    for couple in conjonctives :
        number_treated += 1
        litterals = couple[0]
        conjonctive = couple[1]
        # Getting all values
        node_numbers = 2**(len(litterals.keys())) # Total number of possibilities (= combination of litteral values)
        start = time.time()
        solutions = DPLL.solve(litterals, conjonctive)
        end = time.time()
        exec_time = end - start

        # Starting writing log
        file_title = f"./log/sat_solver_{number_treated}_{datetime.datetime.today()}.txt"
        file_title = file_title.replace(":", "_")  # To ensure windows compatibility
        f = open(file_title, "w")
        f.write(f"Number of possibilities : {node_numbers}\n")
        f.write(f"Number of solutions found : {len(solutions)}\n")
        f.write(f"\n Execution time : {exec_time}s\n\n")
        f.write("Solutions found :\n")
        for element in solutions :
            f.write(f"- {element}\n")
        f.close()


write_results(get_conjonctives("./load.txt"))


