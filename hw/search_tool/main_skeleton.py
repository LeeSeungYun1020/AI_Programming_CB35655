# 201645825 이승윤
from problem import Numeric, Tsp
from optimizer import SteepestAscent, FirstChoice, GradientDescent

problem_type = {
    "1": {
        "name": "Numerical Optimization",
        "problem": Numeric(),
        "algorithm": ["Steepest-Ascent", "First-Choice", "Gradient Descent"]
    },
    "2": {
        "name": "TSP",
        "problem": Tsp(),
        "algorithm": ["Steepest-Ascent", "First-Choice"]
    }
}

algorithm_type = {
    "Steepest-Ascent": SteepestAscent(),
    "First-Choice": FirstChoice(),
    "Gradient Descent": GradientDescent()
}


def select_problem_type():
    """ return problem, problem_code"""
    while True:
        print("Select the problem type:")
        for i, pt in problem_type.items():
            print("\t{}. {}".format(i, pt["name"]))

        index = input("Enter the number: ")
        if index in problem_type:
            return problem_type[index]["problem"], index
        else:
            print("Error: Not exist type\n")


def select_algorithm(problem_code):
    """ return search algorithm"""
    algorithm = {str(i + 1): algo for i, algo in enumerate(problem_type[problem_code]["algorithm"])}
    print()
    while True:
        print("Select the search algorithm:")
        for i, algo in algorithm.items():
            print("\t{}. {}".format(i, algo))

        index = input("Enter the number: ")
        if index in algorithm:
            return algorithm_type[algorithm[index]]
        else:
            print("Error: Not exist algorithm\n")


def main():
    p, p_code = select_problem_type()
    p.setVariables()

    a = select_algorithm(p_code)
    a.setVariables(p)

    a.run()
    p.describe()
    a.displaySetting()
    p.report()


main()
