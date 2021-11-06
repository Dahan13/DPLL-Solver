import matplotlib.pyplot as plt
import numpy as np
import time
from source import DPLL
from source import CNF_generator
import datetime

def graph(n_max, function,sample_mean = 1, only_one_solution = False):
    """ mode: 
     0 = naive 
     1 = first satisfy 
     2 = first fail """
    yt_n=[0 for i in range(n_max+1)]
    yc_n=[0 for i in range(n_max+1)]
    yt_s=[0 for i in range(n_max+1)]
    yc_s=[0 for i in range(n_max+1)]
    yt_f=[0 for i in range(n_max+1)]
    yc_f=[0 for i in range(n_max+1)]
    x=[i for i in range(n_max+1)]
    for n in x:
        litterals, conjonctive = function(n, False)
        
        # Naive 
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive, only_one_solution, 0)
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
            solutions, counter = DPLL.solve(litterals, conjonctive, only_one_solution, 1)
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
            solutions, counter = DPLL.solve(litterals, conjonctive, only_one_solution, 2)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc_f[n] = np.mean(counter_list)
        yt_f[n] = np.mean(t_list)
    
    # start ploting
    # time 
    fig1 = plt.figure()
    plt.plot(x,yt_n,label="Naive")
    plt.plot(x,yt_s,label="First Satisfy")
    plt.plot(x,yt_s,label="First Fail")
    plt.title(f"Time for {function} \nmean over {sample_mean}")
    plt.xlabel("Number of litterals")
    plt.ylabel("Time of résolution")
    plt.yscale("log")
    plt.legend()
    plt.savefig("./graph_result/test.png")
    plt.savefig(f"./graph_result/time_pigeon_{n_max}litterals_mean{sample_mean}.png")

    # nodes 
    fig2 = plt.figure()
    plt.plot(x,yc_n, label="Naive")
    plt.plot(x,yc_s,label="First Satisfy")
    plt.plot(x,yc_s,label="First Fail")
    plt.title(f"Nodes for {function} \nmean over {sample_mean}")
    plt.xlabel("Number of litterals")
    plt.ylabel("Number of nodes explored")
    plt.yscale("log")
    plt.legend()
    plt.savefig(f"./graph_result/nodes_pigeon_{n_max}litterals_mean{sample_mean}.png")


graph(5,CNF_generator.generate_pigeon)