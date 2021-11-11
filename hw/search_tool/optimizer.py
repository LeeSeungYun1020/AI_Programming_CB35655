from abc import abstractmethod
from setup import Setup


class HillClimbing(Setup):
    def __init__(self):
        super().__init__()
        self._limitStuck = 100

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def displaySetting(self):
        pass


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
    self._value = valueC

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
    self._value = valueC