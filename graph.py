import matplotlib.pyplot as plt
import numpy as np
import time
from source import DPLL
from source import CNF_generator
import datetime
try:
    import winsound
    is_windows = True
except:
    is_windows = False

def make_noise():
  duration = 1000  # milliseconds
  freq = 440  # Hz
  winsound.Beep(freq, duration)

def graph(n_max, function, sample_mean = 1):
    yt_n=[0 for i in range(n_max+1)]
    yc_n=[0 for i in range(n_max+1)]
    yt_s=[0 for i in range(n_max+1)]
    yc_s=[0 for i in range(n_max+1)]
    yt_f=[0 for i in range(n_max+1)]
    yc_f=[0 for i in range(n_max+1)]
    x=[i for i in range(n_max+1)]

    # prep parameters
    if function == CNF_generator.generate_pigeon:
        legend = "Number of pigeons"
        name = f"{function.__name__}_{n_max}pigeons_mean{sample_mean}_{datetime.datetime.today()}"
    elif function == CNF_generator.generate_queens:
        legend = "Number of queens"
        name = f"{function.__name__}_{n_max}queens_mean{sample_mean}_{datetime.datetime.today()}"
    elif function == CNF_generator.generate_conjonctive:
        choice = int(input("Increment on litterals (1) or on number of clauses (2) : "))
        if choice == 1:
            legend = "Number of litterals"
            n_second= int(input("Enter number of clauses : "))
            name = f"{function.__name__}_{n_max}litterals_F{n_second}clauses_mean{sample_mean}_{datetime.datetime.today()}"
        elif choice == 2:
            legend = "Number of clauses"
            n_second= int(input("Enter number of litterals : "))
            name = f"{function.__name__}_F{n_second}litterals_{n_max}clauses_mean{sample_mean}_{datetime.datetime.today()}"
        else:
            print("Invalid parameter")
            return
    else:
        print("Invalid function")
        return


    # Calculation
    for n in x:      
        if function == CNF_generator.generate_conjonctive: # ! Complexity over 9000 
            if choice == 1:
                print("1")
                litterals, conjonctive = function(n, n_second, saving = False)
            elif choice == 2:
                print("2")
                litterals, conjonctive = function(n_second, n, saving = False) 
        else:
            litterals, conjonctive = function(n, saving = False)

        # Naive 
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive,mode = 0)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_n[n] = np.mean(counter_list)
        yt_n[n] = np.mean(t_list)

        # First satisfy
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive,mode = 1)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_s[n] = np.mean(counter_list)
        yt_s[n] = np.mean(t_list)

        # First fail
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive, mode = 2)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_f[n] = np.mean(counter_list)
        yt_f[n] = np.mean(t_list)

        # Progression
        pourcentage = round((n/n_max)*100, 2)
        print(f"{pourcentage}%",end="\r")

    

    # Start ploting
    # time 
    fig1 = plt.figure()
    plt.plot(x,yt_n,label="Naive")
    plt.plot(x,yt_s,label="First Satisfy")
    plt.plot(x,yt_s,label="First Fail")
    plt.title(f"Time for {function.__name__} \nmean over {sample_mean}")
    plt.xlabel(legend)
    plt.ylabel("Time of résolution (s)")
    plt.legend()
    
    file_title = f"./graph_result/time_{name}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)
    
    plt.yscale("log")
    file_title = f"./graph_result/time_log_{name}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)
    
    # nodes 
    fig2 = plt.figure()
    plt.plot(x,yc_n, label="Naive")
    plt.plot(x,yc_s,label="First Satisfy")
    plt.plot(x,yc_s,label="First Fail")
    plt.title(f"Nodes for {function.__name__} \nmean over {sample_mean}")
    plt.xlabel(legend)
    plt.ylabel("Number of nodes explored")
    plt.legend()

    file_title = f"./graph_result/nodes_{name}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)

    plt.yscale("log")
    file_title = f"./graph_result/nodes_log_{name}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)

    print("\nDone")
    if is_windows:
        make_noise()        
    else:
        next


graph(9,CNF_generator.generate_pigeon,sample_mean=3)