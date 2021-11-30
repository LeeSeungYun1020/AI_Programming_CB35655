# 201645825 이승윤
import math
import os
import os.path
import random
from abc import abstractmethod
from setup import Setup


class Optimizer(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0
        self._numExp = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._pType = parameters["pType"]
        self._numExp = parameters["numExp"]

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:  # Numerical Problem except gradient descent
            print("Mutation step size:", self._delta)

    def run(self, p):
        p.initProblem()


class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__()
        self._numRestart = 0
        self._limitStuck = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._numRestart = parameters["numRestart"]
        self._limitStuck = parameters["limitStuck"]

    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        super().displaySetting()

    def randomRestart(self, p):
        self.run(p)
        bestSolution = p.getSolution()
        bestMin = p.getValue()

        # if os.path.isfile("tem_re.txt") and self._pType == 2:
        #     os.replace("tem_re.txt", "tem.txt")

        for i in range(1, self._numRestart):
            self.run(p)
            if bestMin > p.getValue():
                bestSolution = p.getSolution()
                bestMin = p.getValue()

        #         if os.path.isfile("tem_re.txt") and self._pType == 2:
        #             os.replace("tem_re.txt", "tem.txt")
        #
        # if os.path.isfile("tem_re.txt"):
        #     os.remove("tem_re.txt")

        p.storeResult(bestSolution, bestMin)

    def run(self, p):
        super().run(p)


class FirstChoice(HillClimbing):

    def run(self, p):
        super().run(p)
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        # file = open("tem_re.txt", "w")
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        #     file.write("{:.3f}\n".format(valueC))
        # file.close()
        p.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        super().displaySetting()
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))


class SteepestAscent(HillClimbing):

    def run(self, p):
        super().run(p)
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            (successor, valueS) = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        super().displaySetting()

    @staticmethod
    def bestOf(neighbors, p):
        evals = [p.evaluate(n) for n in neighbors]
        bestValue = min(evals)
        best = neighbors[evals.index(bestValue)]
        return best, bestValue


class GradientDescent(HillClimbing):

    def run(self, p):
        super().run(p)
        current = p.randomInit()  # Current point
        current_value = p.evaluate(current)

        while True:
            next_point = p.takeStep(current, current_value)
            next_value = p.evaluate(next_point)
            if next_value >= current_value:
                break
            else:
                current = next_point
                current_value = next_value
        p.storeResult(current, current_value)

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivative:", self._dx)
        super().displaySetting()


class Stochastic(HillClimbing):

    def run(self, p):
        super().run(p)
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            neighbors = p.mutants(current)
            (successor, valueS) = self.stochasticBest(neighbors, p)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Stochastic Hill Climbing")
        super().displaySetting()
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))

    # Stochastic hill climbing generates multiple neighbors and then selects
    # one from them at random by a probability proportional to the quality.
    # You can use the following code for this purpose.

    def stochasticBest(self, neighbors, p):
        # Smaller values are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1  # avoid 0
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s:  # The one with index i is chosen / 해당 구간에 속하면
                break
            else:
                s += valuesForMax[i + 1]
        return neighbors[i], valuesForMin[i]


class MetaHeuristics(Optimizer):

    def __init__(self):
        super().__init__()
        self._limitEval = 0
        self._whenBestFound = 0

    def getWhenBestFound(self):
        return self._whenBestFound

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._limitEval = parameters["limitEval"]

    def displaySetting(self):
        super().displaySetting()
        print("Number of evaluations until termination: {:,}".format(self._limitEval))

    def run(self, p):
        super().run(p)


class SimulatedAnnealing(MetaHeuristics):

    def __init__(self):
        super().__init__()
        self._numSample = 100

    def run(self, p):
        super().run(p)
        current = p.randomInit()
        valueC = p.evaluate(current)
        best, valueBest = current, valueC
        whenBestFound = i = 1
        temp = self.initTemp(p)

        # file = ""
        # if self._pType == 2:
        #     file = open("tem.txt", "w")

        while True:
            temp = self.tSchedule(temp)
            if temp == 0 or i == self._limitEval:
                break  # return current
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            i += 1
            dE = valueN - valueC

            if dE < 0 or random.random() < math.exp(-dE / temp):
                current = neighbor
                valueC = valueN

            if valueC < valueBest:
                best, valueBest = current, valueC
                whenBestFound = i

        #     if file:
        #         file.write("{:.3f}\n".format(valueC))
        # if file:
        #     file.close()
        self._whenBestFound = whenBestFound
        p.storeResult(best, valueBest)

    def displaySetting(self):
        print()
        print("Search algorithm: Simulated Annealing")
        print()
        super().displaySetting()

    # Simulated annealing calls the following methods.
    # initTemp returns an initial temperature such that the probability of
    # accepting a worse neighbor is 0.5, i.e., exp(–dE/t) = 0.5.
    # tSchedule returns the next temperature according to an annealing schedule.

    def initTemp(self, p):  # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()  # A random point
            v0 = p.evaluate(c0)  # Its value
            c1 = p.randomMutant(c0)  # A mutant
            v1 = p.evaluate(c1)  # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)  # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10 ** 4))


class GA(MetaHeuristics):

    def __init__(self):
        MetaHeuristics.__init__(self)
        self._popSize = 0  # Population size
        self._uXp = 0  # Probability of swappping a locus for Xover
        self._mrF = 0  # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0  # Crossover rate for permutation code
        self._mR = 0  # Mutation rate for permutation code
        self._pC = 0  # Probability parameter for Xover
        self._pM = 0  # Probability parameter for mutation

    def run(self, p):
        super().run(p)
        # population: list of individuals
        # individual: [fitness, chromosome]
        population = p.initializePop(self._popSize)
        best = self.evalAndFindBest(population, p)

        while p.getNumEval() < self._limitEval:
            new_population = []
            while len(new_population) < self._popSize:
                parent1, parent2 = self.selectParents(population)
                child1, child2 = p.crossover(parent1, parent2, self._pC)
                p.mutation(child1, self._pM)
                p.mutation(child2, self._pM)
                new_population.append(child1)
                new_population.append(child2)

            population = new_population
            new_best = self.evalAndFindBest(population, p)
            if new_best[0] < best[0]:
                best = new_best
                self._whenBestFound = p.getNumEval()

        p.storeResult(p.indToSol(best), best[0]) # store bestSolution, bestValue

    def evalAndFindBest(self, pop, p):
        best = pop[0]
        p.evalInd(best)
        for i in range(1, len(pop)):
            p.evalInd(pop[i])
            if pop[i][0] < best[0]:
                best = pop[i]
        return best

    def selectParents(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1, ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1, ind2)
        return par1, par2

    def selectTwo(self, pop):
        return random.sample(pop, 2)

    def binaryTournament(self, ind1, ind2):
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2

    def setVariables(self, parameters):
        MetaHeuristics.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1: # Numerical optimization
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2: # TSP
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        MetaHeuristics.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:  # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2:  # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)
