import numpy as np
import matplotlib.pyplot as plt
import argparse


def analyticalSolution(x, r, center):
    if abs(center - x) <= r * 1000:
        y = (
            1.0 * 10 ** -8 * (abs(center - x) / 1000)
        ) / (
            2 * 8.85 * 10 ** -12
        )
    else:
        y = (
            1.0 * 10 ** -8 * r ** 2
        ) / (
            2 * 8.85 * 10 ** -12 * abs(center - x) / 1000
        )
    return y


def analyticalSolutionArray(x, y, r, length):
    for i in range(length):
        y[i] = analyticalSolution(x[i], r, x[int(length / 2)])
    return y


def compNumAna(path) -> None:
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
    longitudinalEField = np.zeros(length)
    for i in range(length):
        longitudinalEField[i] = np.sqrt(
            Ex[i][int(length / 2)] ** 2
            + Ey[i][int(length / 2)] ** 2
        )
    horizontalAxis = np.arange(0, 101, 101 / length)
    anaEfield = analyticalSolutionArray(
        horizontalAxis,
        np.zeros(length),
        0.005,
        length
    )
    ax.plot(
        horizontalAxis,
        longitudinalEField,
        marker='.',
        linestyle='None',
        color='blue',
        label='numerical solution'
    )
    ax.plot(
        horizontalAxis,
        anaEfield,
        color='red',
        label='analytical solution'
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 3.0)
    ax.set_title("Electric Field [V/m]")
    ax.set_xlabel("y [mm]")
    ax.set_ylabel("Electric Field [V/ m]")
    ax.legend()
    plt.show()
    return


parser = argparse.ArgumentParser(
    description="fuck"
)

parser.add_argument("data_path", help="data directory path")
args = parser.parse_args()

compNumAna(args.data_path)
