from time import sleep


def countdown(sec):
    while sec > 0:
        print(sec, end="... ")
        sec -= 1
        sleep(1)
    print()
