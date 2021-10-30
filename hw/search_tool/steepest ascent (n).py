from numeric import *
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting("Steepest-Ascent Hill Climbing", DELTA)
    # Report results
    displayResult(solution, minimum, NumEval)


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval

    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def mutants(current, p): ###
    neighbors = [mutate(current, i, DELTA, p) for i in range(len(p[1][0]))]
    neighbors.extend([mutate(current, i, -DELTA, p) for i in range(len(p[1][0]))])
    return neighbors     # Return a set of successors


def bestOf(neighbors, p): ###
    evals = [evaluate(n, p) for n in neighbors]
    bestValue = min(evals)
    best = neighbors[evals.index(bestValue)]
    return best, bestValue


main()
