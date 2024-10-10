import numpy as np
import matplotlib.pyplot as plt
import argparse
from setChargeDensity import halfOfElectrode


def showEPotential(path) -> None:
    try:
        EPotential = np.loadtxt(path, delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()
    length = len(EPotential)

    fig.colorbar(
        ax.imshow(EPotential, cmap='viridis', interpolation='none')
    ).set_label("Electric Potential [V]")
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    ax.set_title("Electric Potential")
    plt.show()
    return


def showElectricChargeDensity(path) -> None:
    try:
        chargeDensityDArray = np.loadtxt(path, delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()
    length = len(chargeDensityDArray)

    fig.colorbar(
        ax.imshow(chargeDensityDArray, cmap='viridis', interpolation='none')
    ).set_label("Electric Charge Density [C/m^3]")
    ax.set_xticks(np.arange(0, length, 10))
    ax.set_yticks(np.arange(0, length, 10))
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    ax.set_title("Electric Charge Density")
    plt.show()
    return


def showEField(path) -> None:
    try:
        Ex = np.loadtxt(path + "/Ex.csv", delimiter=',')
        Ey = np.loadtxt(path + "/Ey.csv", delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()
    length = len(Ex)
    if length != len(Ey):
        print("\033[38;5;196mError: Different number of arrays.\033[0m]")
        return
    magunitudeE = np.zeros((length, length))
    for i in range(length):
        for j in range(length):
            magunitudeE[i][j] = np.sqrt(Ex[i][j] ** 2 + Ey[i][j] ** 2)
    fig.colorbar(
        ax.imshow(magunitudeE, cmap='viridis', interpolation='none')
    ).set_label("Electric Field [V/m]")
    ax.set_xticks(np.arange(0, length, 10))
    ax.set_yticks(np.arange(0, length, 10))
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    # ax.streamplot(
    #     np.arange(0, length, 1),
    #     np.arange(0, length, 1),
    #     Ex,
    #     Ey,
    #     color='blue',
    #     broken_streamlines=False,
    #     density=1
    # )
    ax.set_title("Electric Field")
    plt.show()
    return


def _testShowChargeDensity(a, b) -> None:
    size = 0.1  # 0.1 m
    number = 101
    delta = size / number
    chargeDensity = 1.0 * 10 ** -8

    chargeDensityDArray = halfOfElectrode(a, b, number, delta, chargeDensity)
    np.savetxt(
        "./../data/chargeDensity.csv",
        chargeDensityDArray,
        delimiter=","
    )
    showElectricChargeDensity("./../data/chargeDensity.csv")
    return


parser = argparse.ArgumentParser(
    description="fuck"
)
parser.add_argument("data_path", help='data directory path')
parser.add_argument("-ep", "--electric_potential", action="store_true")
parser.add_argument("-t", "--test", action="store_true")
parser.add_argument("-ef", "--electric_field", action="store_true")
parser.add_argument("-cd", "--charge_density", action="store_true")
args = parser.parse_args()

if (args.charge_density):
    showElectricChargeDensity(args.data_path + "/chargeDensity.csv")
if (args.electric_potential):
    showEPotential(args.data_path + "/electricPotential.csv")
if (args.electric_field):
    showEField(args.data_path)
if (args.charge_density and args.test):
    _testShowChargeDensity(0, 50)
