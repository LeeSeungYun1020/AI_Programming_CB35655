# 201645825 이승윤
from numeric import *

LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting("First-Choice Hill Climbing", DELTA)
    # Report results
    displayResult(solution, minimum)


def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
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


def randomMutant(current, p): ###
    i = random.randint(0, len(p[1][0]) - 1)
    d = random.choice([DELTA, -DELTA])
    return mutate(current, i, d, p)  # Return a random successor


main()
