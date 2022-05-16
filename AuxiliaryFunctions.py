import time


def countdown(sec):
    while sec > 0:
        print(sec, end="... ")
        sec -= 1
        time.sleep(1)
    print()
