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
    else:
        print("Invalid function")
        return


    # Calculation
    for n in x:      
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
    plt.plot(x,yt_f,label="First Fail")
    plt.title(f"Time for {function.__name__}")
    plt.xlabel(legend)
    plt.ylabel("Time of resolution (s)")
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
    plt.plot(x,yc_f,label="First Fail")
    plt.title(f"Nodes for {function.__name__}")
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


graph(8,CNF_generator.generate_queens)

if is_windows:
    make_noise()        
else:
    next