# COmpt Week 11
# Genetic Algorithm Group of Solutions
# author:@tassosblackg
# from pysnooper import snoop
import random

# Problem Data 1
cfile1 = 'knapsack_data/problem1/p01_c.txt' # capacity value
pfile1 = 'knapsack_data/problem1/p01_p.txt' # profits values
wfile1 = 'knapsack_data/problem1/p01_w.txt' # weights values
sfile1 = 'knapsack_data/problem1/p01_s.txt' # solution values

# Problem Data 2
cfile2 = 'knapsack_data/problem2/p02_c.txt' # ..
pfile2 = 'knapsack_data/problem2/p02_p.txt' # ..
wfile2 = 'knapsack_data/problem2/p02_w.txt' # ..
sfile2 = 'knapsack_data/problem2/p02_s.txt' # ..

# Problem Data 2
cfile3 = 'knapsack_data/problem3/p03_c.txt' # ..
pfile3 = 'knapsack_data/problem3/p03_p.txt' # ..
wfile3 = 'knapsack_data/problem3/p03_w.txt' # ..
sfile3 = 'knapsack_data/problem3/p03_s.txt' # ..

# Read Data Func
def get_knap_data(c_file, w_file, p_file, s_file):
    '''
    Get Knapsack problem data from 4 different files, each file
    contains numbers and space with new lines between each value

    Input : file names
     c_file: (c->capcity)
     w_file: (w->weights)
     p_file: (p->profits)
     s_file: (s->solution)

    returns lists of integers with the data plus the capacity value
    '''

    with open(c_file,'r') as f1:
        line = f1.readline().strip()
        capacity = int(line)
    with open(w_file,'r') as f2:
        weights = []
        for line in f2:
            weights.append(int(line.strip()))
    with open(p_file,'r') as f3:
        profits = []
        for line in f3:
            profits.append(int(line.strip()))
    with open(s_file,'r') as f4:
        solution_ohe = []
        for line in f4:
            solution_ohe.append(int(line.strip()))

    return capacity, weights,profits,solution_ohe

# Genetic Algorithm
def knapsack(V, W, MAX, popSize, mut, maxGen, percent):
  generation = 0
  pop = generate(V, popSize)
  fitness = getFitness(pop, V, W, MAX)
  while(not test(fitness, percent) and generation < maxGen):
    generation += 1
    pop = newPopulation(pop, fitness, mut)
    fitness = getFitness(pop, V, W, MAX)
  #print(fitness)
  #print(generation)
  print("\n @ Population = ",pop,"\n" )
  print("\nPopulation = ",pop,file=open("population_out.txt","a"))
  return selectElite(pop, fitness)

def generate(V, popSize):
  length = len(V)
  pop = [[random.randint(0,1) for i in range(length)] for j in range(popSize)]
  #print(pop)
  return pop

def getFitness(pop, V, W, MAX):
  fitness = []
  for i in range(len(pop)):
    weight = 0
    volume = MAX+1
    while (volume > MAX):
      weight = 0
      volume = 0
      ones = []
      for j in range(len(pop[i])):
        if pop[i][j] == 1:
          volume += V[j]
          weight += W[j]
          ones += [j]
      if volume > MAX:
        pop[i][ones[random.randint(0, len(ones)-1)]] = 0
    fitness += [weight]
  #print( "Modified Population:")
  #print( pop)
  #print( "Fitness of Population:")
  #print( fitness)
  return fitness


def newPopulation(pop, fit, mut):
  popSize = len(pop)
  newPop = []
  newPop += [selectElite(pop, fit)]
  #print( "Elite:")
  #print( newPop)
  while(len(newPop) < popSize):
    (mate1, mate2) = select(pop, fit)
    newPop += [mutate(crossover(mate1, mate2), mut)]

  #print( "After Selection")
  #print( newPop)
  return newPop

# Return best solution based on profit
def selectElite(pop, fit):
  elite = 0
  for i in range(len(fit)):
    if fit[i] > fit[elite]:
      elite = i
  return pop[elite]

def select(pop, fit):
  size = len(pop)
  totalFit = sum(fit)
  lucky = random.randint(0, totalFit)
  tempSum = 0
  mate1 = []
  fit1 = 0
  for i in range(size):
    tempSum += fit[i]
    if tempSum >= lucky:
      mate1 = pop.pop(i)
      fit1 = fit.pop(i)
      break
  tempSum = 0
  lucky = random.randint(0, sum(fit))
  for i in range(len(pop)):
    tempSum += fit[i]
    if tempSum >= lucky:
      mate2 = pop[i]
      pop += [mate1]
      fit += [fit1]
      return (mate1, mate2)

# random number of points to crossover
def crossover(mate1, mate2):
  lucky = random.randint(0, len(mate1)-1)
  #print( "Lucky: " + str(lucky))
  return mate1[:lucky]+mate2[lucky:]

def mutate(gene, mutate):
  for i in range(len(gene)):
    lucky = random.randint(1, mutate)
    if lucky == 1:
      #print("MUTATED!")
      gene[i] = bool(gene[i])^1
  return gene

# test if an end of the Algorithm has come
def test(fit, rate):
  maxCount = mode(fit)
  if float(maxCount)/float(len(fit)) >= rate:
    return True
  else:
    return False

def mode(fit):
  values = set(fit) # get all unique fit values
  maxCount = 0
  for i in values:
    if maxCount < fit.count(i):
      maxCount = fit.count(i)
  return maxCount



capacity,weights,profits,best_solution_ohe = get_knap_data(cfile1,wfile1,pfile1,sfile1)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile2,wfile2,pfile2,sfile2)
# capacity,weights,profits,solution_ohe = get_knap_data(cfile3,wfile3,pfile3,sfile3)

print("\n |Number of Items : ",len(profits) )
print("\n |Max capacity of sack: ",capacity)
print("\n |Best solution given as input data: ",best_solution_ohe)

population_size = 30
mutation_denominator = 100 # random selection one value out of 100 or 1/mutation_denominator | end range of random func
numofGen = 5*len(weights) # number of iterations
convegence_percentage = 0.8

selection_list=knapsack(profits, weights, capacity, population_size, mutation_denominator, numofGen, convegence_percentage)
print(selection_list)
print('Elite solution = ', selection_list, file=open("output.txt", "a"))
