import matplotlib.pyplot as plt
import numpy as np
import time
from source import DPLL
from source import CNF_generator
import datetime

def graph(n_litterals_max, function, sample_mean = 1, size_of_conjonctive = 1):
    """ mode: 
     0 = naive 
     1 = first satisfy 
     2 = first fail """
    yt_n=[0 for i in range(n_litterals_max+1)]
    yc_n=[0 for i in range(n_litterals_max+1)]
    yt_s=[0 for i in range(n_litterals_max+1)]
    yc_s=[0 for i in range(n_litterals_max+1)]
    yt_f=[0 for i in range(n_litterals_max+1)]
    yc_f=[0 for i in range(n_litterals_max+1)]
    x=[i for i in range(n_litterals_max+1)]
    for n_litterals in x:
        if function == CNF_generator.generate_conjonctive:
            print("WIP")
            return 
            litterals, conjonctive = function(n_litterals, size_of_conjonctive, saving = False) # ! We need to rethink how to increment on both parameters
        else:
            litterals, conjonctive = function(n_litterals, saving = False)

        # Naive 
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive,mode = 0)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_n[n_litterals] = np.mean(counter_list)
        yt_n[n_litterals] = np.mean(t_list)

        # First satisfy
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive,mode = 1)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_s[n_litterals] = np.mean(counter_list)
        yt_s[n_litterals] = np.mean(t_list)

        # First fail
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive, mode = 2)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_f[n_litterals] = np.mean(counter_list)
        yt_f[n_litterals] = np.mean(t_list)
    
    # start ploting
    # time 
    fig1 = plt.figure()
    plt.plot(x,yt_n,label="Naive")
    plt.plot(x,yt_s,label="First Satisfy")
    plt.plot(x,yt_s,label="First Fail")
    plt.title(f"Time for {function.__name__} \nmean over {sample_mean}")
    plt.xlabel("Number of litterals")
    plt.ylabel("Time of résolution")
    # plt.yscale("log")
    plt.legend()
    file_title = f"./graph_result/time_{function.__name__}_{n_litterals_max}litterals_mean{sample_mean}_{datetime.datetime.today()}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)

    # nodes 
    fig2 = plt.figure()
    plt.plot(x,yc_n, label="Naive")
    plt.plot(x,yc_s,label="First Satisfy")
    plt.plot(x,yc_s,label="First Fail")
    plt.title(f"Nodes for {function.__name__} \nmean over {sample_mean}")
    plt.xlabel("Number of litterals")
    plt.ylabel("Number of nodes explored")
    # plt.yscale("log")
    plt.legend()
    file_title = f"./graph_result/nodes_{function.__name__}_{n_litterals_max}litterals_mean{sample_mean}_{datetime.datetime.today()}.png"
    file_title = file_title.replace(":", "_") 
    plt.savefig(file_title)
    


graph(5,CNF_generator.generate_conjonctive)