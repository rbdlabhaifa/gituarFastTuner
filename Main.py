import Constants
from PitchDetector import tuner
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
    y = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    x = [45, 54, 62.5, 70.5, 77.5, 84.2, 90.3, 96]
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

    print (lagrange_interpolation(x,y))

    print (lagrange_interpolation(x,y))



