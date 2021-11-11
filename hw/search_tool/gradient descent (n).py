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
    currentP = p.randomInit()  # Current point
    valueC = p.evaluate(currentP)
    while True:
        nextP = p.takeStep(currentP, valueC)
        valueN = p.evaluate(nextP)
        if valueN >= valueC:
            break
        else:
            currentP = nextP
            valueC = valueN
    p.storeResult(currentP, valueC)


def gradientDescent(self, alpha=0.01, tol=0.00001, max_iteration=1000):
    self._algorithm = "Gradient descent"
    self._delta = alpha

    current = np.array(self.randomInit())
    valueC = self.evaluate(current)
    step_size = 1
    num_iteration = 0

    while step_size > tol and num_iteration < max_iteration:
        preview = current
        valueP = valueC
        current, valueC = self.takeStep(current)
        step_size = abs(valueC - valueP)
        num_iteration += 1

    self._solution = current
    self._objective_value = valueC


def displaySetting(p):
    print()
    print("Search algorithm: Gradient Descent")
    print()
    print("Udate rate:", p.getAlpha())
    print("Increment for calculating derivative:", p.getDx())

main()
