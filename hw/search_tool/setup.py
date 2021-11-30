# 201645825 이승윤

class Setup:
    def __init__(self):
        self._aType = 0
        self._delta = 0.01
        self._alpha = 0.01
        self._dx = 10 ** (-4)
        self._resolution = 10

    def setVariables(self, parameters):
        self._aType = parameters["aType"]
        self._delta = parameters["delta"]
        self._alpha = parameters["alpha"]
        self._dx = parameters["dx"]
        self._resolution = parameters["resolution"]

    def getAType(self):
        return self._aType
