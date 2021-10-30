import random


def createProblem():  ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    file_name = input("Enter the file name of a function: ")
    with open(file_name, "r") as file:
        expression = file.readline()
        var_names = []
        low = []
        up = []
        for line in file:
            n, l, u = line.rstrip().split(",")
            var_names.append(n)
            l = float(l)
            u = float(u)
            if l > u:
                l, u = u, l
            low.append(l)
            up.append(u)
        domain = [var_names, low, up]
    return expression, domain



def randomInit(p):  ###
    init = [random.uniform(p[1][1][i], p[1][2][i]) for i in range(0, len(p[1][0]))]
    return init  # Return a random initial point
    # as a list of values



def mutate(current, i, d, p):  ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]  # [VarNames, low, up]
    l = domain[1][i]  # Lower bound of i-th
    u = domain[2][i]  # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy



def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])  # Expression
    print("Search space:")
    varNames = p[1][0]  # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i]))



def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple



def displaySetting(algorithm, delta):
    print()
    print("Search algorithm:", algorithm)
    print()
    print("Mutation step size:", delta)


def displayResult(solution, minimum, numEval):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(numEval))

