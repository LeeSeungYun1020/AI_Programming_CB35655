import random
import math
import numpy as np
from abc import abstractmethod


class Problem:
    def __init__(self):
        # Evaluations
        self._num_eval = 0
        # Solution (local min)
        self._solution = []
        # Cost
        self._objective_value = 0
        # Algorithm
        self._algorithm = "undefined"
        # Delta
        self._delta = 0.01

    def firstChoice(self, delta=0.01, limit_stuck=100):
        self._algorithm = "First-Choice Hill Climbing"
        self._delta = delta

        current = self._randomInit()
        valueC = self._evaluate(current)
        i = 0
        while i < limit_stuck:
            successor = self._randomMutant(current)
            valueS = self._evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        self._solution = current
        self._objective_value = valueC

    def steepestAscent(self, delta=0.01):
        self._algorithm = "Steepest-Ascent Hill Climbing"
        self._delta = delta

        current = self._randomInit()
        valueC = self._evaluate(current)
        while True:
            neighbors = self._mutants(current)
            (successor, valueS) = self._bestOf(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        self._solution = current
        self._objective_value = valueC

    @abstractmethod
    def createProblem(self):
        pass

    @abstractmethod
    def describeProblem(self):
        pass

    def displaySetting(self):
        print()
        print("Search algorithm:", self._algorithm)

    @abstractmethod
    def displayResult(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._num_eval))

    @abstractmethod
    def _randomInit(self):
        pass

    @abstractmethod
    def _evaluate(self, current):
        pass

    @abstractmethod
    def _randomMutant(self, current):
        pass

    @abstractmethod
    def _mutants(self, current):
        pass

    @abstractmethod
    def _bestOf(self, neighbors):
        pass


class Numeric(Problem):
    def __init__(self):
        super().__init__()
        self.__expression = ""
        self.__var_names = []
        self.__low = []
        self.__up = []

    def createProblem(self):  ###
        file_name = input("Enter the file name of a function: ")
        with open(file_name, "r") as file:
            self.__expression = file.readline()
            self.__var_names = []
            self.__up = []
            self.__low = []
            for line in file:
                n, l, u = line.rstrip().split(",")
                self.__var_names.append(n)
                l = float(l)
                u = float(u)
                if l > u:
                    l, u = u, l
                self.__low.append(l)
                self.__up.append(u)

    def _randomInit(self):  ###
        init = [random.uniform(self.__low[i], self.__up[i]) for i in range(0, len(self.__var_names))]
        return init  # Return a random initial point as a list of values

    def _evaluate(self, current):
        self._num_eval += 1
        for i in range(len(self.__var_names)):
            assignment = self.__var_names[i] + '=' + str(current[i])
            exec(assignment)
        return eval(self.__expression)

    def __mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        l = self.__low[i]  # Lower bound of i-th
        u = self.__up[i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describeProblem(self):
        print()
        print("Objective function:")
        print(self.__expression)
        print("Search space:")

        for i in range(len(self.__var_names)):
            print(" " + self.__var_names[i] + ":", (self.__low[i], self.__up[i]))

    @staticmethod
    def __coordinate(solution):
        c = [round(value, 3) for value in solution]
        return tuple(c)  # Convert the list to a tuple

    def displaySetting(self):
        super().displaySetting()
        print()
        print("Mutation step size:", self._delta)

    def displayResult(self):
        print()
        print("Solution found:")
        print(self.__coordinate(self._solution))  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._objective_value))
        super().displayResult()

    def _mutants(self, current):  ###
        neighbors = [self.__mutate(current, i, self._delta) for i in range(len(self.__var_names))]
        neighbors.extend([self.__mutate(current, i, -self._delta) for i in range(len(self.__var_names))])
        return neighbors  # Return a set of successors

    def _bestOf(self, neighbors):  ###
        evals = [self._evaluate(n) for n in neighbors]
        bestValue = min(evals)
        best = neighbors[evals.index(bestValue)]
        return best, bestValue

    def _randomMutant(self, current):  ###
        i = random.randint(0, len(self.__var_names) - 1)
        d = random.choice([self._delta, -self._delta])
        return self.__mutate(current, i, d)  # Return a random successor

    def gradientDescent(self, alpha=0.01, tol=0.00001, max_iteration=1000):
        self._algorithm = "Gradient descent"
        self._delta = alpha

        current = np.array(self._randomInit())
        valueC = self._evaluate(current)
        step_size = 1
        num_iteration = 0

        while step_size > tol and num_iteration < max_iteration:
            preview = current
            valueP = valueC
            current, valueC = self.__step(current)
            step_size = abs(valueC - valueP)
            num_iteration += 1

        self._solution = current
        self._objective_value = valueC

    def __derivative(self, current, epsilon=0.0001):
        d = []
        for i in range(len(current)):
            n_current = current.copy()
            n_current[i] += epsilon
            d.append((self._evaluate(n_current) - self._evaluate(current)) / epsilon)
        return np.array(d)

    def __step(self, current):
        change = current - self._delta * self.__derivative(current)  # delta = alpha(learning rate)
        if (np.array(self.__low) <= change).all() and (change <= np.array(self.__up)).all():
            current = change
        value = self._evaluate(current)
        return current, value


class Tsp(Problem):

    def __init__(self):
        super().__init__()
        self.__num_cities = 0
        self.__locations = []
        self.__table = []

    def createProblem(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        self.__num_cities = int(infile.readline())
        self.__locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self.__locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        self.__calcDistanceTable()

    @staticmethod
    def __calcDistance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def __calcDistanceTable(self):  ###
        table = [
            [self.__calcDistance(self.__locations[i], self.__locations[j])
             for j in range(0, self.__num_cities)]
            for i in range(0, self.__num_cities)
        ]
        self.__table = table  # A symmetric matrix of pairwise distances

    def _randomInit(self):  # Return a random initial tour
        init = list(range(self.__num_cities))
        random.shuffle(init)
        return init

    def _evaluate(self, current):  ###
        ## Calculate the tour cost of 'current'
        ## 'current' is a list of city ids
        self._num_eval += 1

        cost = 0
        for i in range(len(current) - 1):
            cost += self.__table[current[i]][current[i + 1]]
        return cost

    @staticmethod
    def __inversion(current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describeProblem(self):
        print()
        n = self.__num_cities
        print("Number of cities:", n)
        print("City locations:")
        locations = self.__locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def __tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()

    def displayResult(self):
        print()
        print("Best order of visits:")
        self.__tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._objective_value)))
        super().displayResult()

    def _randomMutant(self, current):  # Apply inversion
        while True:
            i, j = sorted([random.randrange(self.__num_cities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.__inversion(current, i, j)
                break
        return curCopy

    def _mutants(self, current):  # Apply inversion
        n = self.__num_cities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.__inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def _bestOf(self, neighbors):  ###
        evals = [self._evaluate(n) for n in neighbors]
        bestValue = min(evals)
        best = neighbors[evals.index(bestValue)]
        return best, bestValue
