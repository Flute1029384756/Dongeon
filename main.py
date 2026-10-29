from sys import exit
from pygame import init, quit
from Management.Management_général import Root


def main():
    init()

    jeu_global = Root()
    jeu_global.jeu()

    quit()
    exit()


if __name__ == "__main__":
    main()
