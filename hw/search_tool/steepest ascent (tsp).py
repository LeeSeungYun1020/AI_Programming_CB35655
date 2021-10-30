# 201645825 이승윤
from tsp import *


def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting("Steepest-Ascent Hill Climbing")
    # Report results
    displayResult(solution, minimum)


def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors


def bestOf(neighbors, p): ###
    evals = [evaluate(n, p) for n in neighbors]
    bestValue = min(evals)
    best = neighbors[evals.index(bestValue)]
    return best, bestValue


main()
