import matplotlib.pyplot as plt
import numpy as np
import time
from source import DPLL
from source import CNF_generator

def graph(n_max, function, mode,sample_mean = 1, only_one_solution = False):
    """ mode: 
     0 = naive 
     1 = first satisfy 
     2 = first fail """
    yt=[0 for i in range(n_max+1)]
    yc=[0 for i in range(n_max+1)]
    x=[i for i in range(n_max+1)]
    for n in x:
        litterals, conjonctive = function(n, False)
        t_list=[]
        counter_list = []
        for i in range(sample_mean):
            ts= time.time()
            solutions, counter = DPLL.solve(litterals, conjonctive, only_one_solution, mode)
            te= time.time()
            t_list.append(te-ts)
            counter_list.append(counter)
        yc[n] = np.mean(counter_list)
        yt[n] = np.mean(t_list)
    
    # start ploting
    # time first
    fig1 = plt.figure()
    plt.plot(x,yt,label="Naive")
    plt.legend()

    # nodes second
    fig2 = plt.figure()
    plt.plot(x,yc, label="Naive")

    plt.show()

graph(2,CNF_generator.generate_pigeon,0)