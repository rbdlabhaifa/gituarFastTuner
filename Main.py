import Constants
from PitchDetector import tuner

def main():
    target_note = input("please select note you which to tune to: E4, B3, G3, D3, A2, E2")
    notes_dict = {}
    notes_dict['E4'] = 329.6
    notes_dict['B3'] = 246.9
    notes_dict['G3'] = 196
    notes_dict['D3'] = 143.8
    notes_dict['A2'] = 110
    notes_dict['E2'] = 82.4
    target_pitch = notes_dict[target_note]

    tuner()

    current_pitch = max(set(Constants.PITCH_LIST), key=Constants.PITCH_LIST.count)
    distance_to_pitch = target_pitch - current_pitch
    print(f"you are {distance_to_pitch} away from your target!")






if __name__ == "__main__":
    main()


