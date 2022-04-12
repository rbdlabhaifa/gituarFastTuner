import Constants
from PitchDetector import PitchDetector
from matplotlib.pyplot import plot, title, xlabel, ylabel, gcf
from numpy import polyfit, linspace, polyval

def lagrange_interpolation(x, y, xp):
    yp = 0
    for i in range(len(x)):
        p = 1
        for j in range(len(x)):
            if i != j:
                p = p * (xp - x[j]) / (x[i] - x[j])
        yp = yp + p * y[i]
    return (yp)


def get_samples(note):
    y6 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    x6 = [45, 54, 62.5, 70.5, 77.5, 84.2, 90.3, 96]
    y5 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    x5 = [52.2, 58.2, 69, 77.9, 86.8, 94, 102, 108.1, 115.1]
    y4 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]
    x4 = [56, 66, 77, 86.5, 96.5, 104.4, 113, 120, 128.2, 134.7, 141.5, 147, 154, 159.8, 165.5, 170.1, 175, 179, 183.5,
          187.1]
    y3 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5]
    x3 = [70.5, 81.3, 94.2, 105.5, 117.1, 126.3, 136, 144, 152.7, 160, 167.7, 174.6, 182, 188.2, 195, 200.5, 207, 211.4,
          216.5, 220.5, 225, 229, 233.3, 236.7]
    y2 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]
    x2 = [96.7, 115, 138, 157, 176, 190, 210, 223, 239.3, 251.5, 265.5, 276.7]
    y1 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5]
    x1 = [158.8, 172.5, 194.3, 211.3, 230, 245.7, 261.5, 275, 290, 302.2, 315.8, 326.5, 338.5, 348, 359, 367.3]

    if note == 'E4':
        return x1,y1
    elif note == 'B3':
        return x2, y2
    elif note == 'G3':
        return x3, y3
    elif note == 'D3':
        return x4, y4
    elif note == 'A2':
        return x5, y5
    elif note == 'E2':
        return x6, y6
    else:
        return 0


if __name__ == "__main__":
    notes_dict = {'E4': 329.6, 'B3': 246.9, 'G3': 196, 'D3': 143.8, 'A2': 110, 'E2': 82.4}
    pitchdetector = PitchDetector(Constants.ALL_NOTES, Constants.OCTAVE_BANDS, 13)
    while True:
        target_note = input("Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n").upper()
        if target_note in notes_dict:
            target_pitch = notes_dict[target_note]

            break
        else:
            print("Illegal input, please try again...")
    x, y = get_samples(target_note)
    pitchdetector.detect()
    current_pitch = max(set(pitchdetector.detected_pitches), key=pitchdetector.detected_pitches.count)
    print(f"detected pitch: {current_pitch}")
    distance_to_pitch = lagrange_interpolation(x, y, target_pitch) - lagrange_interpolation(x, y, current_pitch)
    print(f"distance_to_pitch: {distance_to_pitch}")

    print("please tune your note ")
    print(distance_to_pitch * 360)
    print(" degrees")



