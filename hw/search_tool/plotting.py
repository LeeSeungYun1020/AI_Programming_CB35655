import matplotlib.pyplot as plt
import numpy as np


def main():
    firstChoice = np.loadtxt("alg2.txt")
    simulatedAnnealing = np.loadtxt("alg5.txt")
    plt.title("Progress of Search")
    plt.plot(firstChoice)
    plt.plot(simulatedAnnealing)
    plt.legend(["First choice", "Simulated annealing"])
    plt.xlabel("evaluations")
    plt.ylabel("cost")
    plt.show()


main()
