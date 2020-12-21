import numpy as np
import random

def generateRandomPopulation(size, lenght=-1):
    if lenght != -1:
        pop = np.random.randint(32,126,size=(size,lenght))
    else:
        pop = np.empty(size, dtype=object)
        for i in range(size):
            pop[i] = np.random.randint(32,126, size=(1,random.randint(0,21))).flatten()
    return pop

def showPopulation(pop):
    for ind in pop:
        string = ""
        for n in ind:
            string += chr(n)
        print(string)

pop = generateRandomPopulation(15, lenght=-1)
print(pop)
showPopulation(pop)