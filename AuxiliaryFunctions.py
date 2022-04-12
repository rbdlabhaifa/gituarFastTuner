import time

def lagrange_interpolation(x, y, xp):
    yp = 0
    for i in range(len(x)):
        p = 1
        for j in range(len(x)):
            if i != j:
                p = p * (xp - x[j]) / (x[i] - x[j])
        yp = yp + p * y[i]
    return (yp)


def countdown(sec):
    while sec > 0:
        print(sec, end="... ")
        sec -= 1
        time.sleep(1)
    print()
