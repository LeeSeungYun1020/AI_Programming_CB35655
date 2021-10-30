# 201645825 이승윤
from tsp import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, distanceTable)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting("First-Choice Hill Climbing")
    # Report results
    displayResult(solution, minimum)


def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


def randomMutant(current, p): # Apply inversion
    while True:
        i, j = sorted([random.randrange(p[0])
                       for _ in range(2)])
        if i < j:
            curCopy = inversion(current, i, j)
            break
    return curCopy


main()
