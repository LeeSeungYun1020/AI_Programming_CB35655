# 201645825 이승윤
from problem import Tsp


def main():
    tsp = Tsp()
    # Create an instance of TSP
    tsp.createProblem()
    # Call the search algorithm
    tsp.firstChoice()
    # Show the problem and algorithm settings
    tsp.describeProblem()
    tsp.displaySetting()
    # Report results
    tsp.displayResult()


main()
