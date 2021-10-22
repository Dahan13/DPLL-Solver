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
    for raw_conjonctive in conjonctive_list:
        



print(separate_conjonctives(load_conjonctive("./load.txt")))