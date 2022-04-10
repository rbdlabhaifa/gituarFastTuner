import Constants
from PitchDetector import PitchDetector
from matplotlib.pyplot import plot, title, xlabel, ylabel, gcf
from numpy import polyfit, linspace, polyval


def lagrange_interpolation(x, y):
    xp = float(input('Enter interpolation point: '))
    yp = 0
    for i in range(len(x)):
        p = 1
        for j in range(len(x)):
            if i != j:
                p = p * (xp - x[j]) / (x[i] - x[j])
        yp = yp + p * y[i]
    return (yp)


if __name__ == "__main__":
    notes_dict = {'E4': 329.6, 'B3': 246.9, 'G3': 196, 'D3': 143.8, 'A2': 110, 'E2': 82.4}
    y1 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    x1 = [45, 54, 62.5, 70.5, 77.5, 84.2, 90.3, 96]
    y2 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    x2 = [52.2, 58.2, 69, 77.9, 86.8, 94, 102, 108.1, 115.1]
    y3 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]
    x3 = [56, 66, 77, 86.5, 96.5, 104.4, 113, 120, 128.2, 134.7, 141.5, 147, 154, 159.8, 165.5, 170.1, 175, 179, 183.5,
          187.1]
    y4 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5]
    x4 = [70.5, 81.3, 94.2, 105.5, 117.1, 126.3, 136, 144, 152.7, 160, 167.7, 174.6, 182, 188.2, 195, 200.5, 207, 211.4,
          216.5, 220.5, 225, 229, 233.3, 236.7]
    y5 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
    x5 = [96.7, 115, 138, 157, 176, 190, 210, 223, 239.3, 251.5, 265.5, 276.7]
    y6 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5]
    x6 = [158.8, 172.5, 194.3, 211.3, 230, 245.7, 261.5, 275, 290, 302.2, 315.8, 326.5, 338.5, 348, 359, 367.3
          ]

    # while True:
    #     target_note = input("Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n").upper()
    #     if target_note in notes_dict:
    #         target_pitch = notes_dict[target_note]
    #         break
    #     else:
    #         print("Illegal input, please try again...")
    # tuner()
    # current_pitch = max(set(Constants.PITCH_LIST), key=Constants.PITCH_LIST.count)
    # distance_to_pitch = target_pitch - current_pitch
    # print(f"You are {distance_to_pitch} away from your target!")

    print(lagrange_interpolation(x, y))

    print(lagrange_interpolation(x, y))
