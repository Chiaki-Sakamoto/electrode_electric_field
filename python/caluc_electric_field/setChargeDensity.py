import numpy as np


def makeElectrodeFacingSemicircle(a, b, number, delta, chargeDensity):
    chargeDensityDArray = np.zeros((number, number))
    length = len(chargeDensityDArray)

    for y in range(length):
        for x in range(length):
            if (
                (
                    y * delta >= (b + 3.75) / 1000
                    or y * delta <= (b - 3.75) / 1000
                ) and
                (
                    x * delta >= (a + 20) / 1000
                    and x * delta <= (a + 24.7) / 1000
                )
                and (a / 1000 - x * delta) ** 2 + (b / 1000 - y * delta) ** 2
                <= 0.025 ** 2
            ):
                chargeDensityDArray[y][x] = chargeDensity
            if (
                (
                    y * delta >= (b + 3.75) / 1000
                    or y * delta <= (b - 3.75) / 1000
                ) and
                (
                    x * delta >= (a + 29.7) / 1000
                    and x * delta <= (a + 34.4) / 1000
                )
                and ((a + 54.4) / 1000 - x * delta) ** 2
                + (b / 1000 - y * delta) ** 2 <= 0.025 ** 2
            ):
                chargeDensityDArray[y][x] = chargeDensity
    return chargeDensityDArray


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
