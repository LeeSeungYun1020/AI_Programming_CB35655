# 201645825 이승윤
from abc import abstractmethod
from setup import Setup
from problem import Numeric


class HillClimbing(Setup):
    def __init__(self):
        super().__init__()
        self._limitStuck = 100

    def setVariables(self, parameters):
        self._problem = problem

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def displaySetting(self):
        pass


class FirstChoice(HillClimbing):

    def run(self):
        current = self._problem.randomInit()  # 'current' is a list of values
        valueC = self._problem.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = self._problem.randomMutant(current)
            valueS = self._problem.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        self._problem.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        if isinstance(self._problem, Numeric):
            print()
            print("Mutation step size:", self._delta)
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))


class SteepestAscent(HillClimbing):

    def run(self):
        current = self._problem.randomInit()  # 'current' is a list of values
        valueC = self._problem.evaluate(current)
        while True:
            neighbors = self._problem.mutants(current)
            (successor, valueS) = self.bestOf(neighbors, self._problem)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        self._problem.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        if isinstance(self._problem, Numeric):
            print()
            print("Mutation step size:", self._delta)

    @staticmethod
    def bestOf(neighbors, p):
        evals = [p.evaluate(n) for n in neighbors]
        bestValue = min(evals)
        best = neighbors[evals.index(bestValue)]
        return best, bestValue


class GradientDescent(HillClimbing):
    def run(self):
        current = self._problem.randomInit()  # Current point
        current_value = self._problem.evaluate(current)

        while True:
            next_point = self._problem.takeStep(current, current_value)
            next_value = self._problem.evaluate(next_point)
            if next_value >= current_value:
                break
            else:
                current = next_point
                current_value = next_value
        self._problem.storeResult(current, current_value)

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivative:", self._dx)
