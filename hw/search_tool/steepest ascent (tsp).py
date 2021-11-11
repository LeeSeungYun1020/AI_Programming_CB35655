# 201645825 이승윤
from problem import Tsp


def main():
    p = Tsp()
    # Create an instance of TSP
    p.setVariables()
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()

def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)


def bestOf(self, neighbors):
    evals = [self.evaluate(n) for n in neighbors]
    bestValue = min(evals)
    best = neighbors[evals.index(bestValue)]
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
