import json
from PitchDetector import PitchDetector
from AuxiliaryFunctions import countdown
from ConfigSections import *


class GuitarTuner:
    def __init__(self):
        self.frequencies = {"E4": 329.63, "B3": 246.94, "G3": 196.00, "D3": 146.83, "A2": 110.00, "E2": 82.41}
        self.frequency_change_per_degree = {"E4": 15 / 180, "B3": 13.5 / 180, "G3": 12 / 180, "D3": 5 / 180,
                                            "A2": 4.5 / 180, "E2": 4 / 180}
        self.octave_bands = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
        self.notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

        # Getting the adjusted frequency changes from config
        self.config = json.load(open('config.json'))
        if FREQUENCY_CHANGES_PER_DEGREE in self.config:
            frequency_changes = self.config[FREQUENCY_CHANGES_PER_DEGREE]
            for change in frequency_changes:
                self.frequency_change_per_degree[change] = frequency_changes[change]

        # Getting the target note from user
        self.target_note = ''
        legal_note = False
        while not legal_note:
            self.target_note = input('Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n').upper()
            if self.target_note not in self.frequencies:
                print("Illegal note, please try again...")
            else:
                legal_note = True

    def detect_pitch(self):
        pitch_detector = PitchDetector(self.notes, self.octave_bands, self.config[DETECTOR_ITERATIONS])
        pitch_detector.detect()
        return pitch_detector.detected_pitch

    def is_tuned(self, distance_to_pitch):
        frequency_change = self.frequency_change_per_degree[self.target_note]
        if -5 * frequency_change < distance_to_pitch < 5 * frequency_change:
            print(f"{self.target_note} is tuned.")
            return True
        return False

    def print_tuning_instruction(self, distance_to_pitch):
        frequency_change = self.frequency_change_per_degree[self.target_note]
        if distance_to_pitch > 0:
            print(f"Strengthen {round(distance_to_pitch / frequency_change)} degrees")
        else:
            print(f"Release {round(-distance_to_pitch / frequency_change)} degrees")

    def adjust_frequency_change(self, prev_distance, first_pitch, second_pitch):
        frequency_change = self.frequency_change_per_degree[self.target_note]

        # Adjusting the frequency change factor
        adjusted_degrees = abs(prev_distance) / frequency_change
        frequency_change = abs(first_pitch - second_pitch) / adjusted_degrees
        self.frequency_change_per_degree[self.target_note] = frequency_change

        # Saving the new frequency changes to config
        self.config[FREQUENCY_CHANGES_PER_DEGREE] = self.frequency_change_per_degree
        f = open('config.json', 'w')
        json.dump(self.config, f)

    def tune_note(self):
        target_pitch = self.frequencies[self.target_note]
        print(f"Target pitch: {target_pitch}")

        first_detected_pitch = self.detect_pitch()
        print(f"First detected pitch: {first_detected_pitch}")

        distance_to_pitch = target_pitch - first_detected_pitch
        if self.is_tuned(distance_to_pitch):
            # The note is already tuned
            return

        self.print_tuning_instruction(distance_to_pitch)
        print("Going again in", end=' ')
        countdown(self.config[COUNTDOWN_FROM])

        second_detected_pitch = self.detect_pitch()
        print(f"Second detected pitch: {second_detected_pitch}")
        if not self.is_tuned(target_pitch - second_detected_pitch):
            # Need to adjust the frequency changes
            self.adjust_frequency_change(distance_to_pitch, first_detected_pitch, second_detected_pitch)
            self.print_tuning_instruction(target_pitch - second_detected_pitch)
