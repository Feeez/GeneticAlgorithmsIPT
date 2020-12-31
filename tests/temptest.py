import numpy as np
import random
from string import ascii_letters
charset = [ord(c) for c in ascii_letters + " +-*/'0123456789!?.,;:"] #define charset as characters like ()@é^[]{} are not allowed. Charset is the list of ascii numbers of allowed characters

def coder(mot):
    A = 'M*T-rEs/.oL:int64'
    B = len(A)
    C = ascii_letters + " +-*/'0123456789!?.,;:"
    return( bytes([ord(C[(C.index(c)+ord(A[i%B]))%74]) for i,c in enumerate(mot)]) )    

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
    return pop2str(pop)

def pop2str(pop):
    """
        returns the population bus as a string np array
        pop : (np array population) the population to convert
    """
    strPop = np.empty(len(pop), dtype=object)   #using the empty method is faster than creating an array
    for i in range(len(pop)):
        strPop[i] = ""
        for n in pop[i]: # iterate through each individual
            strPop[i] += chr(charset[n])   # converts char by char from an index in the allowed char set into a letter
    return strPop

def individualScore(pop, secret, codingFunction=lambda x : x):
    """
        returns a np array containing scores associated with each individual
        pop : (np array population) the population to estimate
        secret : (bytes) the secret phrase to compare the population to
        codingFunction : (function / lambda) the function used to code secret
    """
    scores = np.empty(len(pop), dtype=int)
    for i in range(len(pop)):
        coded = codingFunction(pop[i])  #encode the current indivudual in order to do it only once
        scores[i] = 10 * (len(secret) - len(coded))**2   #high importance is set to length difference (raised to power 2 and multiplicative factor)

        for j in range(min(len(coded), len(secret))):   #iterate on the more little between the secret phrase and the individual in order to avoid index problems
            scores[i] += abs(coded[j] - secret[j])      #score is defined by de difference betweend ascii numbers for each character in the individual's string  
    return scores

def childrenAllocation(couples, childrenNumber):
    """
        returns the number of child each couple will produce on the next generation
        couples : (np array couples) the couples formed among the population
        childrenNumber : Number of children to distribute among couples
    """
    
    remainingChildren = childrenNumber
    children = np.zeros(len(couples), dtype=int)

    while remainingChildren >= len(couples):    #if possible, give a child to every couple
        children += 1                       #using the numpy implementation for addition on an entire array
        remainingChildren -= len(couples)
    
    for coupleIndex in random.sample(range(len(couples)), remainingChildren): #randomly give one more child to couples, whithout giving one twice to the same couple (random.sample does it well)
        children[coupleIndex] += 1

    return children

def newChild(p1, p2, cut=-1):
    """
        creates a new child from two parents, cutting strings at a certain index
        p1 : (string) parent 1
        p2 : (string) parent 2
        cut : (int) cutting index - leave -1 to cut in the middle (50 %) - use with caution, won't work properly if cut exceeds the length of parents
    """
    child = ""
    if cut == -1:
        child = p1[:len(p1)//2] + p2[len(p2)//2:]   #using string slicing to take half of each parent
    else:
        child = p1[:min(len(p1), cut)] + p2[min(len(p2), cut):] #using slicing to cut at the right place - using the min() function to avoid the IndexOutOfRange error
    return child

def rePopulate(pop, couples, children, childrenNumber):
    """
        create the new generation
        pop : (np array population) current purged population
        couples : (np array couples) couples between individuals
        children : (np array children) number of children per couple
        childrenNumber :(int) total number of children that will be created
    """
    newPop = np.empty(childrenNumber, dtype=object)   #empty array that will contain new children
    currentChild = 0    #index to follow the insertion of children into the array
    for coupleIndex in range(len(couples)): #iterate through every couple to create its children
        for n in range(children[coupleIndex]):  #create as many children as stored in the "children" array
            newPop[currentChild] = newChild(pop[couples[coupleIndex][0]],pop[couples[coupleIndex][1]])
            currentChild += 1
    return np.hstack((pop,newPop))  #concatenate two arrays : old and new population


def mutate(ind, m):
    mutated = ""
    for char in ind:
        p = random.random()
        if p <= (m/2) / len(ind):
            mutated += chr(charset[random.randint(0,len(charset)-1)])
        else:
            mutated += char
    
    p = random.random()
    if p <= m / 4:
        pos = random.randint(0,len(mutated))
        mutated = mutated[:pos] + mutated[(pos+1):]
    
    p = random.random()
    if p <= m / 4:
        pos = random.randint(0,len(mutated))
        mutated = mutated[:pos] + chr(charset[random.randint(0,len(charset)-1)]) + mutated[pos:]
    return mutated


#print(newChild("testbleu","rouetest"),newChild("testbleu","rouetest",cut=100))
#pop = generateRandomPopulation(10, length=4)
#print(pop)
#print(individualScore(pop, coder("test"), coder))
#couples = np.array([[0,1],[2,3],[4,5],[6,7],[8,9]])
#print(couples)
#children = childrenAllocation(couples, 5)
#newPop = rePopulate(pop, couples, children, 5)
#print(newPop)
c=0
for i in range(100):
    mutated = mutate("testbleurouge", 0.1)
    if mutated != "testbleurouge":
        c += 1
print(c/100)