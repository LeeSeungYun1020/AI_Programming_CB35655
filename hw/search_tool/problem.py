# 201645825 이승윤
import random
import math
import numpy as np
from abc import abstractmethod
from setup import Setup


class Problem(Setup):
    def __init__(self):
        super().__init__()
        # Evaluations
        self._num_eval = 0
        # Solution (local min)
        self._solution = []
        # Cost
        self._value = 0
        self._pFileName = ""

        self._bestSolution = []
        self._bestMinimum = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._sumOfNumEval = 0
        self._avgWhen = 0

    def setVariables(self, parameters):
        self._pFileName = parameters["pFileName"]

    def getNumEval(self):
        return self._num_eval

    def getSolution(self):
        return self._solution

    def getValue(self):
        return self._value

    def randomInit(self):
        self._num_eval = 0
        self._solution = []
        self._value = 0

    @abstractmethod
    def evaluate(self, current):
        pass

    @abstractmethod
    def mutants(self, current):
        pass

    @abstractmethod
    def randomMutant(self, current):
        pass

    @abstractmethod
    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def storeExpResult(self, results):
        (self._bestSolution, self._bestMinimum, self._avgMinimum,
         self._avgNumEval, self._sumOfNumEval, self._avgWhen) = results

    def report(self):
        print()
        print("Average objective value: {0:,.3f}".format(self._avgMinimum))
        print("Average number of evaluations: {0:,}".format(self._avgNumEval))
        self.reportDetail()
        print()
        print("Total number of evaluations: {0:,}".format(self._sumOfNumEval))

    @abstractmethod
    def reportDetail(self):
        pass


class Numeric(Problem):
    def __init__(self):
        super().__init__()
        self._expression = ""
        self._var_names = []
        self._low = []
        self._up = []

    def setVariables(self, parameters):
        super().setVariables(parameters)
        with open(self._pFileName, "r") as file:
            self._expression = file.readline()
            self._var_names = []
            self._up = []
            self._low = []
            for line in file:
                n, l, u = line.rstrip().split(",")
                self._var_names.append(n)
                l = float(l)
                u = float(u)
                if l > u:
                    l, u = u, l
                self._low.append(l)
                self._up.append(u)

    def randomInit(self):
        super().randomInit()
        init = [random.uniform(self._low[i], self._up[i]) for i in range(0, len(self._var_names))]
        return init  # Return a random initial point as a list of values

    def evaluate(self, current):
        self._num_eval += 1
        for i in range(len(self._var_names)):
            assignment = self._var_names[i] + '=' + str(current[i])
            exec(assignment)
        return eval(self._expression)

    def mutants(self, current):
        neighbors = [self.mutate(current, i, self._delta) for i in range(len(self._var_names))]
        neighbors.extend([self.mutate(current, i, -self._delta) for i in range(len(self._var_names))])
        return neighbors  # Return a set of successors

    def mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        l = self._low[i]  # Lower bound of i-th
        u = self._up[i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):
        i = random.randint(0, len(self._var_names) - 1)
        d = random.choice([self._delta, -self._delta])
        return self.mutate(current, i, d)  # Return a random successor

    def takeStep(self, current, current_value):
        change = current - self._alpha * self.gradient(current, current_value)
        if self.isLegal(change):
            current = change
        return current

    def gradient(self, current, current_value):
        d = []
        for i in range(len(current)):
            n_current = current.copy()
            n_current[i] += self._dx
            d.append((self.evaluate(n_current) - current_value) / self._dx)
        return np.array(d)

    def isLegal(self, x):
        return (np.array(self._low) <= x).all() and (x <= np.array(self._up)).all()

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)
        print("Search space:")

        for i in range(len(self._var_names)):
            print(" " + self._var_names[i] + ":", (self._low[i], self._up[i]))

    def reportDetail(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._bestMinimum))

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):

    def __init__(self):
        super().__init__()
        self._num_cities = 0
        self._locations = []
        self._table = []

    def setVariables(self, parameters):
        super().setVariables(parameters)
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        infile = open(self._pFileName, 'r')
        # First line is number of cities
        self._num_cities = int(infile.readline())
        self._locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.calcDistanceTable()

    @staticmethod
    def calcDistance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def calcDistanceTable(self):
        table = [
            [self.calcDistance(self._locations[i], self._locations[j])
             for j in range(0, self._num_cities)]
            for i in range(0, self._num_cities)
        ]
        self._table = table  # A symmetric matrix of pairwise distances

    def randomInit(self):  # Return a random initial tour
        super().randomInit()
        init = list(range(self._num_cities))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        ## Calculate the tour cost of 'current'
        ## 'current' is a list of city ids
        self._num_eval += 1
        cost = 0
        for i in range(len(current) - 1):
            cost += self._table[current[i]][current[i + 1]]
        return cost

    def mutants(self, current):  # Apply inversion
        n = self._num_cities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    @staticmethod
    def inversion(current, i, j):  ## Perform inversion
        mutant = current[:]
        while i < j:
            mutant[i], mutant[j] = mutant[j], mutant[i]
            i += 1
            j -= 1
        return mutant

    def randomMutant(self, current):  # Apply inversion
        while True:
            i, j = sorted([random.randrange(self._num_cities)
                           for _ in range(2)])
            if i < j:
                mutant = self.inversion(current, i, j)
                break
        return mutant

    def describe(self):
        print()
        n = self._num_cities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def reportDetail(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._bestMinimum)))

    def tenPerRow(self):
        for i in range(len(self._bestSolution)):
            print("{0:>5}".format(self._bestSolution[i]), end='')
            if i % 10 == 9:
                print()
