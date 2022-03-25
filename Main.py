import Constants
from PitchDetector import tuner


if __name__ == "__main__":
    notes_dict = {'E4': 329.6, 'B3': 246.9, 'G3': 196, 'D3': 143.8, 'A2': 110, 'E2': 82.4}
    while True:
        target_note = input("Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n").upper()
        if target_note in notes_dict:
            target_pitch = notes_dict[target_note]
            break
        else:
            print("Illegal input, please try again...")
    tuner()
    current_pitch = max(set(Constants.PITCH_LIST), key=Constants.PITCH_LIST.count)
    distance_to_pitch = target_pitch - current_pitch
    print(f"You are {distance_to_pitch} away from your target!")

