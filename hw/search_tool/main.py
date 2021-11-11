from problem import Tsp, Numeric

def select_problem_type():
    problem_type = {
        "1": {
            "name": "Numerical Optimization",
            "problem": Numeric()
        },
        "2": {
            "name": "TSP",
            "problem": Tsp()
        }
    }

    print("Select the problem type:")
    for i, pt in problem_type.items():
        print("\t{}. {}".format(i, pt["name"]))
    return problem_type[input("Enter the number: ")]["problem"]

def main():
    p = select_problem_type()
    print(p)

main()