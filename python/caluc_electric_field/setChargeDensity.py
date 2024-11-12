import numpy as np


def makeElectrodeFacingSemicircle(a, b, number, delta, chargeDensity):
    chargeDensityDArray = np.zeros((number, number))
    length = len(chargeDensityDArray)

    for y in range(length):
        for x in range(length):
            if (
                (
                    y * delta >= b + 0.00375
                    or y * delta <= b - 0.00375
                ) and
                (
                    x * delta >= a + 0.020
                    and x * delta <= a + 0.0247
                ) and
                (
                    y * delta - b >=
                    - (6.55 / 4.7) * (x * delta - a) + (8853 / 235000)
                    or y * delta - b <=
                    (6.55 / 4.7) * (x * delta - a) - (8853 / 235000)
                ) and
                (a - x * delta) ** 2 + (b - y * delta) ** 2
                <= 0.025 ** 2
            ):
                chargeDensityDArray[y][x] = chargeDensity
    return chargeDensityDArray


def groundElectrodeSemicircular(a, b, number, delta):
    groundElectrodeDArray = np.zeros((number, number))
    length = len(groundElectrodeDArray)

    for y in range(length):
        for x in range(length):
            if (
                (
                    y * delta > b + 0.00375
                    or y * delta < b - 0.00375
                ) and
                (
                    x * delta > a + 0.0297
                    and x * delta < a + 0.0344
                ) and
                (
                    y * delta - b >
                    (6.55 / 4.7) * (x * delta - a) - (8738 / 235000)
                    or y * delta - b <
                    - (6.55 / 4.7) * (x * delta - a) + (8738 / 235000)
                )
                and ((a + 0.0544) - x * delta) ** 2
                + (b - y * delta) ** 2 < 0.025 ** 2
            ):
                groundElectrodeDArray[y][x] = 1
    return groundElectrodeDArray


def noGroundElectrode(number):
    groundElectrodeDArray = np.zeros((number, number))
    return groundElectrodeDArray


def makeCircularElectrode(a, b, number, delta, chargeDensity):
    chargeDensityDArray = np.zeros((number, number))
    length = len(chargeDensityDArray)

    for y in range(length):
        for x in range(length):
            if (
                (
                    a <= x * delta and x * delta <= a + 0.004
                ) and (
                    b - 0.015 <= y * delta and y * delta <= b + 0.015
                ) and (
                    y * delta - b >= -0.6875 * (x * delta - a) + 0.0065
                    or y * delta - b <= 0.6875 * (x * delta - a) - 0.0065
                )
            ):
                chargeDensityDArray[y][x] = chargeDensity
    return chargeDensityDArray


def groundCircleElectrode(a, b, number, delta):
    groundElectrodeDArray = np.zeros((number, number))
    length = len(groundElectrodeDArray)

    for y in range(length):
        for x in range(length):
            if (
                (
                    a + 0.009 <= x * delta and x * delta <= a + 0.013
                ) and (
                    b - 0.015 <= y * delta and y * delta <= b + 0.015
                ) and (
                    y * delta - b >= 0.6875 * (x * delta - a) - 0.0024375
                    or y * delta - b <= -0.6875 * (x * delta - a) + 0.0024375
                )
            ):
                groundElectrodeDArray[y][x] = 1
    return groundElectrodeDArray


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
