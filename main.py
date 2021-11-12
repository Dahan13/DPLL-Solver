from source import file_management
from source import CNF_generator
try:
    import winsound
    is_windows = True
except:
    is_windows = False

def make_noise():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


def main():
    # Asking for all parameters
    heuristic = int(input("Select your mode, 0 for naive, 1 for first satisfy and 2 for first fail : "))
    if heuristic != 0 and heuristic != 1 and heuristic != 2:
        heuristic = 0
    only_one_solution = input("Do you want only one solution ? (y/n) ")
    if only_one_solution == "y" or only_one_solution == "Y" or only_one_solution == "yes" or only_one_solution == "Yes":
        only_one_solution = True
    else:
        only_one_solution = False
    if not only_one_solution:
        naif = input("Do you want to compare the solver' results with the results of a naive solver ? Be warned that this may takes time. (y/n) ")
        if naif == "y" or naif == "Y" or naif == "yes" or naif == "Yes":
            naif = True
        else:
            naif = False
    else:
        naif = False

    # Asking for which conjonctive we will work on
    conjonc_choice = input("Do you want to load a conjonctive from a file ? (y/n) ")
    if conjonc_choice == "y" or conjonc_choice == "Y" or conjonc_choice == "yes" or conjonc_choice == "Yes":
        file_path = input("Please enter the file path to the conjonctive data : \n")
        file_management.write_results(file_management.get_conjonctives(file_path), only_one_solution, naif, heuristic)
    else:
        conjonc_choice == False
        rand_choice = int(input("Do you want a random conjonctive (0), a pigeon problem (1) or a N-queens problem (2) ? "))
        while rand_choice != 0 and rand_choice != 1 and rand_choice != 2:
            rand_choice = int(input("Sorry I didn't understand...\nRetry : "))
        if rand_choice == 0:
            n_literals = int(input("How many literals do you want ? "))
            n_clauses = int(input("How many clauses do you want ? "))
            file_management.write_results([CNF_generator.generate_conjonctive(n_literals, n_clauses)], only_one_solution, naif, heuristic)
        elif rand_choice == 1:
            n_pigeons = int(input("How many pigeons do you want ? "))
            file_management.write_results([CNF_generator.generate_pigeon(n_pigeons)], only_one_solution, naif, heuristic)
        elif rand_choice == 2:
            n_queens = int(input("Enter the size of the board : "))
            file_management.write_results([CNF_generator.generate_queens(n_queens)], only_one_solution, naif, heuristic)
    if is_windows:
        make_noise()

main()

