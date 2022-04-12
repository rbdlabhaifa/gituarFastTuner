import json
from PitchDetector import PitchDetector
from AuxiliaryFunctions import lagrange_interpolation, countdown

OCTAVE_BANDS = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
ALL_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

if __name__ == "__main__":
    is_tuned = False
    notes_dict = {'E4': 329.6, 'B3': 246.9, 'G3': 196, 'D3': 143.8, 'A2': 110, 'E2': 82.4}

    while True:
        target_note = input("Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n").upper()
        if target_note in notes_dict:
            target_pitch = notes_dict[target_note]

            break
        else:
            print("Illegal input, please try again...")

    f = open('Samples.json')
    samples = json.load(f)
    x, y = samples[target_note]["x"], samples[target_note]["y"]

    while not is_tuned:
        pitch_detector = PitchDetector(ALL_NOTES, OCTAVE_BANDS, 13)
        pitch_detector.detect()
        current_pitch = max(set(pitch_detector.detected_pitches), key=pitch_detector.detected_pitches.count)
        distance_to_pitch = lagrange_interpolation(x, y, target_pitch) - lagrange_interpolation(x, y, current_pitch)

        print(f"Detected pitch: {current_pitch}")
        print(f"Target pitch: {target_pitch}")
        print(f"Distance to target: {round(distance_to_pitch, 3)}")
        print("--------------------------------------------------")

        if -0.02 < distance_to_pitch < 0.02:
            print(f"{target_note} is tuned.")
            is_tuned = True

        else:
            if distance_to_pitch > 0:
                print(f"Strengthen {round(distance_to_pitch * 360)} degrees")
            else:
                print(f"Release {round(-distance_to_pitch * 360)} degrees")
            print("Going again in", end=' ')
            countdown(5)
