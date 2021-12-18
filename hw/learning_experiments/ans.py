import numpy as np


def main():
    print("Which learning algorithm do you want to use?")
    print(" 1. Linear Regression")
    print(" 2. k-NN")
    aType = int(input("Enter the number: "))
    if aType == 1:
        ml = LinearRegression()
    else:
        ml = KNN()
    fileName = input("Enter the file name of training data: ")
    ml.setData('train', fileName)
    fileName = input("Enter the file name of test data: ")
    ml.setData('test', fileName)
    ml.buildModel()
    ml.testModel()
    ml.report()


class ML:
    def __init__(self):
        self._trainDx = np.array([])
        self._trainDy = np.array([])
        self._testDx = np.array([])
        self._testDy = np.array([])
        self._testPy = np.array([])

    def setData(self, dtype, fileName):  # set class variables
        dx, dy = self.createMatrices(fileName)
        if dtype == "train":
            self._trainDx, self._trainDy = dx, dy
        elif dtype == "test":
            self._testDx, self._testDy = dx, dy
            self._testPy = np.zeros(self._testDy.shape)

    def createMatrices(self, fileName):  # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]
            features = data[0:-1]
            target = data[-1]
            XSet.append(features)
            ySet.append(target)
        infile.close()
        XArray = np.array(XSet)
        yArray = np.array(ySet)
        return XArray, yArray

    def testModel(self):  # Test model with the test set
        n = np.size(self._testDy)
        for i in range(n):
            self._testPy[i] = self.runModel(self._testDx[i])

    def report(self):
        n = np.size(self._testDy)  # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2
            totalSe += se
        print()
        print("RMSE: ", round(np.sqrt(totalSe / n), 2))


class LinearRegression(ML):
    def __init__(self):
        ML.__init__(self)
        self._w = np.array([])  # Optimal weights for linear regression

    def buildModel(self):
        X = self._trainDx
        n = np.size(self._trainDy)
        X0 = np.ones([n, 1])
        nX = np.hstack((X0, X))  # Add a column of all 1's as the first column
        y = self._trainDy
        t_nX = np.transpose(nX)
        self._w = np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)

    def runModel(self, data):  # Apply linear regression to a test data
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)


class KNN(ML):
    def __init__(self, k=0):
        ML.__init__(self)
        self._k = k  # k value for k-NN

    def buildModel(self):
        if self._k == 0:
            self._k = int(input("Enter the value for k: "))

    def runModel(self, query):
        closetK = self.findCK(query)
        return self.takeAvg(closetK)

    def findCK(self, query):
        # closetK = np.zeros([self._k, 2], dtype=int)
        closetK = np.arange(2 * self._k).reshape(self._k, 2)
        for i in range(self._k):
            closetK[i][0] = i
            closetK[i][1] = self.sDistance(query, self._trainDx[i])
        for j in range(self._k, len(self._trainDy)):
            self.updateCK(closetK, j, query)
        return closetK

    def sDistance(self, dataA, dataB):
        sum = 0
        for i in range(len(dataA)):
            sum += (dataA[i] - dataB[i]) ** 2
        return sum

    def updateCK(self, closetK, i, query):
        j = np.argmax(closetK[:, 1])
        d = self.sDistance(query, self._trainDx[i])
        if closetK[j][1] > d:
            closetK[j][0] = i
            closetK[j][1] = d

    def takeAvg(self, closetK):
        sum = 0
        for i in range(self._k):
            j = closetK[i][0]
            sum += self._trainDy[j]
        return sum / self._k


main()
