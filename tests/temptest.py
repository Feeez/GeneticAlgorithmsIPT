import numpy as np
import random
from string import ascii_letters
charset = [ord(c) for c in ascii_letters + " +-*/'0123456789!?.,;:"] #define charset as characters like ()@é^[]{} are not allowed. Charset is the list of ascii numbers of allowed characters

def generateRandomPopulation(size, length=-1):
    """
        returns a numpy array containing a population made of ASCII numbers
        size : (int) size of the population
        length : (int) length of each individual (leave blank or -1 for a random length)
    """
    if length != -1:    #if length is fixed - generate a population of that length 
        pop = np.random.randint(0,len(charset),size=(size,length))  #using numpy fo fill an array containing random index of charset
    else:    # - generate a random length population
        pop = np.empty(size, dtype=object)  #create an empty array to fill later
        for i in range(size):
            pop[i] = np.random.randint(0,len(charset), size=(1,random.randint(0,21))).flatten() #fill the array with a random length with a randomly generated list of charset index
    return pop

def showPopulation(pop):
    """
        prints the whole population as strings
        pop : (np array population) the population to print
    """
    for ind in pop:
        string = ""
        for n in ind: # iterate through each individual
            string += chr(charset[n])   # converts char by char from an index in the allowed char set into a letter
        print(string)

pop = generateRandomPopulation(5, length=4)
print(pop)
showPopulation(pop)