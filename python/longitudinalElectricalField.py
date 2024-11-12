import numpy as np
import matplotlib.pyplot as plt
import argparse


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
    longitudinalEField = np.zeros(length)
    for i in range(length):
        longitudinalEField[i] = np.sqrt(
            Ex[i][int(length / 2)] ** 2
            + Ey[i][int(length / 2)] ** 2
        )
    ax.plot(
        np.arange(0, 100, 100 / length),
        longitudinalEField,
        marker='.',
        linestyle='None',
        color='blue'
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 2500000)
    ax.set_title("Electric Field [V/m]")
    ax.set_xlabel("y [mm]")
    ax.set_ylabel("Electric Field [V/ m]")
    plt.show()
    return


parser = argparse.ArgumentParser(
    description="fuck"
)
parser.add_argument("data_path", help="data directory path")
parser.add_argument("-ef", "--electric_field", action="store_true")
args = parser.parse_args()

if (args.electric_field):
    showEField(args.data_path)
