"""Main module."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def computeArea(pos):
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def RCI(pop,disp):
    pop_pr = pop/sum(pop)
    disp_pr = disp/sum(disp)
    pop_pr_sum = []
    disp_pr_sum = []
    for i in range(0,(len(pop)+1)):
        pop_pr_sum.append(sum(pop_pr[0:i]))
        disp_pr_sum.append(sum(disp_pr[0:i]))
    equal = [0,1]
    polygon = plt.fill(np.append(pop_pr_sum, equal[::-1]), np.append(disp_pr_sum, equal[::-1]));
    plt.close()
    return(computeArea(polygon[0].xy)*2)

def ACI(pop,disp,rate):
    pop_pr = pop/sum(pop)
    disp_pr = disp/sum(disp)
    pop_pr_sum = []
    disp_pr_sum = []
    for i in range(0,(len(pop)+1)):
        pop_pr_sum.append(sum(pop_pr[0:i]))
        disp_pr_sum.append(sum(disp_pr[0:i]))
    equal = [0,1]
    polygon = plt.fill(np.append(pop_pr_sum, equal[::-1]), np.append(disp_pr_sum, equal[::-1]));
    plt.close()
    return((computeArea(polygon[0].xy)*2)*(sum(rate)/len(rate)))

def con_curve(pop,disp):
    lc = [0,0.2,0.4,0.6,0.8,1]
    pop_pr = pop/sum(pop)
    disp_pr = disp/sum(disp)
    pop_pr_sum = []
    disp_pr_sum = []
    for i in range(0,(len(pop)+1)):
        pop_pr_sum.append(sum(pop_pr[0:i]))
        disp_pr_sum.append(sum(disp_pr[0:i]))
    plt.plot(pop_pr_sum, disp_pr_sum)
    plt.plot(lc, lc,c='k',linewidth=0.75)
    plt.axis(xmin=0,ymin=0,xmax=1,ymax=1)
