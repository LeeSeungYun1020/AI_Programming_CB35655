# 201645825 이승윤
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

    @abstractmethod
    def displaySetting(self):
        pass


class HillClimbing(Optimizer):
    def __init__(self):
        super().__init__()
        self._numRestart = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._numRestart = parameters["numRestart"]

    def displaySetting(self):
        if self._pType == 1:  # Numerical Problem
            print()
            print("Mutation step size:", self._delta)

    def randomRestart(self, p):
        for i in range(self._numRestart):
            self.run(p)


class FirstChoice(HillClimbing):
    def __init__(self):
        super().__init__()
        self._limitStuck = 0

    def setVariables(self, parameters):
        super().setVariables(parameters)
        self._limitStuck = parameters["limitStuck"]

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
