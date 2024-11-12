import os


def makeDirectory(path) -> None:
    try:
        os.makedirs(path)
    except FileExistsError:
        print("\033[38;5;220mdata directory exist.\033[0m")
    return
