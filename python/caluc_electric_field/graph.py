import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
from setChargeDensity import makeElectrodeFacingSemicircle


def showEPotential(path) -> None:
    try:
        EPotential = np.loadtxt(path, delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()

    fig.colorbar(
        ax.imshow(
            EPotential,
            extent=[0, 100, 0, 100],
            cmap='viridis',
            interpolation='none'
        )
    ).set_label("Electric Potential [V]")
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

    fig.colorbar(
        ax.imshow(
            chargeDensityDArray,
            extent=[0, 100, 0, 100],
            cmap='viridis',
            interpolation='none'
        )
    ).set_label("Electric Charge Density [C/m^2]")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    ax.set_title("Electric Charge Density")
    plt.show()
    return


def showEField(path, lineFlag) -> None:
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
        ax.imshow(
            magunitudeE,
            extent=[0, 100, 0, 100],
            cmap='viridis',
            interpolation='none'
        )
    ).set_label("Electric Field [V/m]")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    if (lineFlag):
        ax.streamplot(
            np.arange(0, length, 1),
            np.arange(0, length, 1),
            Ex,
            Ey,
            color='blue',
            broken_streamlines=False,
            density=0.3
        )
    ax.set_title("Electric Field")
    plt.show()
    return


def showEFieldx(path) -> None:
    try:
        EFieldx = np.loadtxt(path, delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()

    fig.colorbar(
        ax.imshow(
            EFieldx,
            extent=[0, 100, 0, 100],
            cmap='viridis',
            interpolation='none'
        )
    ).set_label("Electric field [V/m]")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    ax.set_title("Electric Field in x direction")
    plt.show()
    return


def showEFieldy(path) -> None:
    try:
        EFieldy = np.loadtxt(path, delimiter=',')
    except FileNotFoundError:
        print("\033[38;5;196mError: Invalid directory path.\033[0m")
        return
    fig, ax = plt.subplots()

    fig.colorbar(
        ax.imshow(
            EFieldy,
            extent=[0, 100, 0, 100],
            cmap='viridis',
            interpolation='none'
        )
    ).set_label("Electric Field [V/m]")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.invert_yaxis()
    ax.set_title("Electric Field in y direction")
    plt.show()
    return


def makeDirectory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("\033[38;5;220mdata directory exist.\033[0m")
    return


def _testShowChargeDensity(a, b, path) -> None:
    size = 0.1  # 0.1 m
    number = 200
    delta = size / number
    chargeDensity = 1.0 * 10 ** -8

    makeDirectory(path)
    chargeDensityDArray = makeElectrodeFacingSemicircle(
        a,
        b,
        number,
        delta,
        chargeDensity
    )
    np.savetxt(
        path + "/chargeDensity.csv",
        chargeDensityDArray,
        delimiter=","
    )
    showElectricChargeDensity(path + "/chargeDensity.csv")
    return


parser = argparse.ArgumentParser(
    description="fuck"
)
parser.add_argument("data_path", help='data directory path')
parser.add_argument("-ep", "--electric_potential", action="store_true")
parser.add_argument("-t", "--test", action="store_true")
parser.add_argument("-ef", "--electric_field", action="store_true")
parser.add_argument("-ex", "--electric_field_x", action="store_true")
parser.add_argument("-ey", "--electric_field_y", action="store_true")
parser.add_argument("-cd", "--charge_density", action="store_true")
parser.add_argument("-lef", "--line_of_electric_force", action="store_true")
args = parser.parse_args()

if (args.charge_density and not args.test):
    showElectricChargeDensity(args.data_path + "/chargeDensity.csv")
if (args.electric_potential):
    showEPotential(args.data_path + "/electricPotential.csv")
if (args.electric_field):
    showEField(args.data_path, args.line_of_electric_force)
if (args.electric_field_x):
    showEFieldx(args.data_path + "/Ex.csv")
if (args.electric_field_y):
    showEFieldy(args.data_path + "/Ey.csv")
if (args.charge_density and args.test):
    _testShowChargeDensity(0.022, 0.05, args.data_path)
