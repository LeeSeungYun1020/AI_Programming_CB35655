# 201645825 이승윤
from problem import Numeric


def main():
    p = Numeric()
    # Create an instance of numerical optimization problem
    p.setVariables()
    # Call the search algorithm
    gradientDescent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()


def gradientDescent(p):
    current = p.randomInit()  # Current point
    current_value = p.evaluate(current)

    while True:
        next_point = p.takeStep(current, current_value)
        next_value = p.evaluate(next_point)
        if next_value >= current_value:
            break
        else:
            current = next_point
            current_value = next_value
    p.storeResult(current, current_value)


def displaySetting(p):
    print()
    print("Search algorithm: Gradient Descent")
    print()
    print("Update rate:", p.getAlpha())
    print("Increment for calculating derivative:", p.getDx())


main()
