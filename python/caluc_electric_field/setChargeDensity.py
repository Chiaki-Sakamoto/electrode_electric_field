import numpy as np


def halfOfElectrode(a, b, number, delta, chargeDensity):
    chargeDensityDArray = np.zeros((number, number))
    length = len(chargeDensityDArray)
    sdelta = delta ** 2

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
                and ((a - x) ** 2 + (b - y) ** 2) * sdelta <= 0.025 ** 2
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
