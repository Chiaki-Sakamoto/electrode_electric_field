import numpy as np
import os
# import matplotlib as plt
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
    def executeCulc(void):
        return


class CalcuEField(ACalcuE):
    def __init__(self, area, number, EChargeDensityDArray) -> None:
        super().__init__(number)
        self._area = area
        self._delta = area / number
        self._EChargeDensityDArray = EChargeDensityDArray
        self._EFieldx = np.zeros((100, 100))
        self._EFieldy = np.zeros((100, 100))
        return

    def __del__(self) -> None:
        return

    def executeCulc(self):
        for i in range(1, super().getNumber() - 1):
            for j in range(1, super().getNumber() - 1):
                self._EFieldx[i][j] = - (
                    self._EChargeDensityDArray[i + 1][j]
                    - self._EChargeDensityDArray[i - 1][j]
                ) / (2.0 * self._delta)
                self._EFieldy[i][j] = -(
                    self._EChargeDensityDArray[i][j + 1]
                    - self._EChargeDensityDArray[i][j - 1]
                ) / (2.0 * self._delta)
        return


class CalcuEPotential(ACalcuE):
    _PrevEPotential = 0

    def __init__(
        self,
        area,
        number,
        chargeDensity,
        chargeDensityDArray
    ) -> None:
        super().__init__(number)
        self._area = area
        self._delta = area / number
        self._maxEPotential = chargeDensity
        self._EChargeDensityDArray = chargeDensityDArray
        self._EPotentialDArray = np.zeros((number, number))
        return

    def __del__(self) -> None:
        return

    def executeCulc(self):
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
                    prevEPotential = self._EPotentialDArray[i][j]
                    self._EPotentialDArray[i][j] = 0.25 * (
                        self._EChargeDensityDArray[i][j] * sDelta
                        / super().getEpsilon0()
                        + self._EPotentialDArray[i + 1][j]
                        + self._EPotentialDArray[i - 1][j]
                        + self._EChargeDensityDArray[i][j + 1]
                        + self._EChargeDensityDArray[i][j - 1]
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
        return


def makeChargeDensityDArray(number, delta, radius, chargeDensity):
    chargeDensityDArray = np.zeros((number, number))
    center = number / 2
    sDelta = delta ** 2
    sRadius = radius ** 2
    for i in range(number):
        for j in range(number):
            if (
                ((center - i) ** 2 + (center - j) ** 2) * sDelta < sRadius
            ):
                chargeDensityDArray[i][j] = chargeDensity
    return chargeDensityDArray


def makeDirectory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("\033[38;5;220mdata directory exist.\033[0m\n")
    return


def outputCulc(path, ePotentialDArray, EFieldx, EFieldy):
    np.savetxt(path+"/electricPotential.csv", ePotentialDArray, delimiter=",")
    np.savetxt(path+"/Ex.csv", EFieldx, delimiter=",")
    np.savetxt(path+"/Ey.csv", EFieldy, delimiter=",")
    return


def main():
    size = 0.1
    number = 100
    delta = size / number
    chargeDensity = 1.0 * 10 ** -8
    path = "./data"

    EPotential = CalcuEPotential(
        size,
        number,
        chargeDensity,
        makeChargeDensityDArray(number, delta, 0.005, chargeDensity)
    )
    EPotential.executeCulc()
    EField = CalcuEField(
        size,
        number,
        EPotential._EPotentialDArray
    )
    EField.executeCulc()
    makeDirectory(path)
    outputCulc(
        path,
        EPotential._EPotentialDArray,
        EField._EFieldx,
        EField._EFieldy
    )
    return (os.EX_OK)
