# 201645825 이승윤
import math
import random
from abc import abstractmethod
from setup import Setup
from problem import Numeric


class Optimizer(Setup):
    def __init__(self):
        super().__init__()
        self._pType = 0
        self._aType = 0
        self._numExp = 0

    def setVariables(self, parameters):
        self._pType = parameters["pType"]
        self._aType = parameters["aType"]
        self._numExp = parameters["numExp"]
        self._delta = parameters["delta"]
        self._alpha = parameters["alpha"]
        self._dx = parameters["dx"]

    def getAType(self):
        return self._aType

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    @abstractmethod
    def run(self, p):
        pass

    def displaySetting(self):
        if self._pType == 1:  # Numerical Problem
            print()
            print("Mutation step size:", self._delta)


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
        print()
        print("Number of random restarts:", self._numRestart)
        super().displaySetting()

    def randomRestart(self, p):
        self.run(p)
        bestSolution = p.getSolution()
        bestMin = p.getValue()
        for i in range(1, self._numRestart):
            self.run(p)
            if bestMin > p.getValue():
                bestSolution = p.getSolution()
                bestMin = p.getValue()
        p.storeResult(bestSolution, bestMin)


class FirstChoice(HillClimbing):

    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        super().displaySetting()
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))


class SteepestAscent(HillClimbing):

    def run(self, p):
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

    # Stochastic hill climbing generates multiple neighbors and then selects
    # one from them at random by a probability proportional to the quality.
    # You can use the following code for this purpose.

    def stochasticBest(self, neighbors, p):
        # Smaller values are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s:  # The one with index i is chosen
                break
            else:
                s += valuesForMax[i + 1]
        return neighbors[i], valuesForMin[i]


class MetaHeuristics(Optimizer):
    def __init__(self):
        super().__init__()
        self._limitEval = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._limitEval = parameters["limitEval"]

    def displaySetting(self):
        print()
        print("Number of limit evaluations:", self._limitEval)
        super().displaySetting()


class SimulatedAnnealing(MetaHeuristics):
    def run(self, p):
        pass

    def displaySetting(self):
        print()
        print("Search algorithm: Simulated Annealing Metaheuristic")
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
