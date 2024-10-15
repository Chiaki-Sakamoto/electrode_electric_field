import os
import numpy as np
import argparse
import time
from .electrodeElectricField import CalcuEField
from .electrodeElectricField import CalcuEPotential
from .setChargeDensity import makeElectrodeFacingSemicircle
from .setChargeDensity import groundElectrodeSemicircular


def makeDirectory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("\033[38;5;220mdata directory exist.\033[0m")
    return


def outputCulc(path, eChargeDensityDArray, ePotentialDArray, EFieldx, EFieldy):
    np.savetxt(
        path + "/chargeDensity.csv",
        eChargeDensityDArray,
        delimiter=","
    )
    np.savetxt(
        path + "/electricPotential.csv",
        ePotentialDArray,
        delimiter=","
    )
    np.savetxt(path + "/Ex.csv", EFieldx, delimiter=",")
    np.savetxt(path + "/Ey.csv", EFieldy, delimiter=",")

    return


def main():
    size = 0.1  # 0.1 m
    number = 300
    delta = size / number
    chargeDensity = 1.0 * 10 ** -8
    parse = argparse.ArgumentParser(
        description="fuck"
    )
    parse.add_argument(
        "directory_path",
        help="directory path",
        default="./data/"
    )
    args = parse.parse_args()
    startTime = time.time()

    EPotential = CalcuEPotential(
        size,
        number,
        chargeDensity,
        makeElectrodeFacingSemicircle(
            0.022,
            0.050,
            number,
            delta,
            chargeDensity
        ),
        groundElectrodeSemicircular(0.022, 0.050, number, delta)
    )
    EPotential.executeCulc()
    EField = CalcuEField(
        size,
        number,
        EPotential._EPotentialDArray
    )
    EField.executeCulc()
    makeDirectory(args.directory_path)
    outputCulc(
        args.directory_path,
        EPotential._EChargeDensityDArray,
        EPotential._EPotentialDArray,
        EField._EFieldx,
        EField._EFieldy
    )
    endTime = time.time()
    elapsedTime = endTime - startTime
    minutes, seconds = divmod(elapsedTime, 60)
    hours, minutes = divmod(minutes, 60)
    print(
        "\033[38;5;202mcalculate time: ",
        hours, "hours, ",
        minutes, "minutes, ",
        int(seconds), "seconds",
        "\033[0m")
    return (os.EX_OK)
