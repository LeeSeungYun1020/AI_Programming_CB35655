# 201645825 이승윤
from problem import Numeric


def main():
    n = Numeric()
    # Create an instance of numerical optimization problem
    n.createProblem()
    # Call the search algorithm
    n.gradientDescent()
    # Show the problem and algorithm settings
    n.describeProblem()
    n.displaySetting()
    # Report results
    n.displayResult()


main()
