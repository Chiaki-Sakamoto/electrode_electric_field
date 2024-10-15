import numpy as np
from abc import ABC, abstractmethod


class ACalcuE(ABC):
    _epsilon0 = 8.85 * 10 ** -12
    _measurementError = 1.0 * 10 ** -6

    def __init__(self, number) -> None:
        self._number = number
        return

    def __del__(self) -> None:
        return

    def getEpsilon0(self):
        return self._epsilon0

    def getMeasurementError(self):
        return self._measurementError

    def getNumber(self):
        return self._number

    @abstractmethod
    def executeCulc(void) -> None:
        return


class CalcuEField(ACalcuE):
    def __init__(self, area, number, EPotentialDArray) -> None:
        super().__init__(number)
        self._area = area
        self._delta = area / number
        self._EPotentialDArray = EPotentialDArray
        self._EFieldx = np.zeros((number, number))
        self._EFieldy = np.zeros((number, number))
        return

    def __del__(self) -> None:
        return

    def executeCulc(self) -> None:
        for i in range(1, super().getNumber() - 1):
            for j in range(1, super().getNumber() - 1):
                self._EFieldx[i][j] = - (
                    self._EPotentialDArray[i][j + 1]
                    - self._EPotentialDArray[i][j - 1]
                ) / (2.0 * self._delta)
                self._EFieldy[i][j] = - (
                    self._EPotentialDArray[i + 1][j]
                    - self._EPotentialDArray[i - 1][j]
                ) / (2.0 * self._delta)
        return


class CalcuEPotential(ACalcuE):
    _PrevEPotential = 0

    def __init__(
        self,
        area,
        number,
        chargeDensity,
        chargeDensityDArray,
        groundElectrodeDArray,
    ) -> None:
        super().__init__(number)
        self._area = area
        self._delta = area / number
        self._maxEPotential = chargeDensity
        self._EChargeDensityDArray = chargeDensityDArray
        self._EPotentialDArray = np.zeros((number, number))
        self._groundElectrodeDArray = groundElectrodeDArray
        return

    def __del__(self) -> None:
        return

    def __singleCoreCulc(self) -> None:
        index = 0
        maxEPotential = 1.0 * 10 ** -10
        maxError = 0.0
        curError = 0.0
        prevEPotential = 0.0
        sDelta = self._delta ** 2

        while True:
            maxError = curError = 0.0
            if (index % 1000):
                print("\033[38;5;87m\rloop: ", index, "\033[0m", end="")
            for i in range(1, super().getNumber() - 1):
                for j in range(1, super().getNumber() - 1):
                    if (self._groundElectrodeDArray[i][j] == 0):
                        prevEPotential = self._EPotentialDArray[i][j]
                        self._EPotentialDArray[i][j] = 0.25 * (
                            self._EChargeDensityDArray[i][j] * sDelta
                            / super().getEpsilon0()
                            + self._EPotentialDArray[i + 1][j]
                            + self._EPotentialDArray[i - 1][j]
                            + self._EPotentialDArray[i][j + 1]
                            + self._EPotentialDArray[i][j - 1]
                        )
                        if (maxEPotential < abs(self._EPotentialDArray[i][j])):
                            maxEPotential = self._EPotentialDArray[i][j]
                        curError = (
                            abs(self._EPotentialDArray[i][j] - prevEPotential)
                        ) / maxEPotential
                        if (maxError < curError):
                            maxError = curError
            index += 1
            if (maxError <= super().getMeasurementError()):
                break
        print("")
        return

    def __multiCoreCulc(self):
        return

    def executeCulc(self) -> None:
        self.__singleCoreCulc()
        return
