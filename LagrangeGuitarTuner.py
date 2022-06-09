from json import load
from PitchDetector import PitchDetector
from AuxiliaryFunctions import countdown
from ConfigSections import *


class LagrangeGuitarTuner:
    def __init__(self):
        self.iterations = 0
        self.frequencies = {"E4": 329.63, "B3": 246.94, "G3": 196.00, "D3": 146.83, "A2": 110.00, "E2": 82.41}
        self.octave_bands = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
        self.notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        f = open('samples.json')
        self.samples = load(f)
        self.config = load(open('config.json'))
        self.target_note = ''

    def detect_pitch(self):
        pitch_detector = PitchDetector(self.notes, self.octave_bands, self.config[DETECTOR_ITERATIONS])
        detected_pitch = pitch_detector.detect()
        return detected_pitch

    def is_tuned(self, distance_to_pitch):
        return -self.config[TUNING_EPSILON] < distance_to_pitch < self.config[TUNING_EPSILON]

    def get_instructions(self, current_pitch, target_pitch):
        lagrange_target = self.lagrange_interpolation(target_pitch)
        lagrange_current = self.lagrange_interpolation(current_pitch)
        print(f"lagrange target: {lagrange_target}")
        print(f"lagrange current: {lagrange_current}")
        return lagrange_current, lagrange_target

    def print_instructions(self, distance_to_pitch):
        degrees_to_pitch = round(distance_to_pitch * 360)
        half_turns_to_pitch = round(degrees_to_pitch / 180)
        turns_to_pitch = half_turns_to_pitch / 2
        reminder_degrees_to_pitch = degrees_to_pitch - (half_turns_to_pitch * 180)
        if turns_to_pitch > 0:
            print(f"Strengthen {abs(turns_to_pitch)} turns and {abs(reminder_degrees_to_pitch)} degrees")
        else:
            print(f"Release {abs(turns_to_pitch)} turns and {abs(reminder_degrees_to_pitch)} degrees")

    def tune_note(self):
        self.select_note()
        target_pitch = self.frequencies[self.target_note]
        print(f"Target pitch: {target_pitch}")
        print("get ready to play!")
        countdown(self.config[START_COUNTDOWN])
        current_pitch = self.detect_pitch()
        print(f"First detected pitch: {current_pitch}")
        distance_to_pitch = target_pitch - current_pitch
        if self.is_tuned(distance_to_pitch):
            print(f"{self.target_note} is tuned.")
            return

        current_turns, target_turns = self.get_instructions(current_pitch, target_pitch)
        self.print_instructions(target_turns - current_turns)
        print("Going again in", end=' ')
        previous_turns = current_turns
        countdown(self.config[INTERMISSION_COUNTDOWN])
        current_pitch = self.detect_pitch()

        while not self.is_tuned(target_pitch - current_pitch) and self.iterations < self.config[TUNER_ITERATIONS]:
            print(f"new detected pitch: {current_pitch}")
            current_turns, target_turns = self.get_instructions(current_pitch, target_pitch)
            print(f"Current turns: {current_turns}")
            print(f"Target turns: {target_turns}")
            off_percentage = (current_turns - previous_turns) / (target_turns - previous_turns)
            print(f"Off percentage: {off_percentage}")
            self.print_instructions((target_turns - current_turns) * (1/off_percentage))
            previous_turns = current_turns
            print("Going again in", end=' ')
            self.iterations += 1
            countdown(self.config[INTERMISSION_COUNTDOWN])
            current_pitch = self.detect_pitch()
        if self.is_tuned(target_pitch - current_pitch):
            print(f"{self.target_note} is tuned.")
            return
        else:
            print(f"new detected pitch: {current_pitch}")
            return

    def lagrange_interpolation(self, pitch):
        equation_result = 0
        x, y = self.samples[self.target_note]["x"], self.samples[self.target_note]["y"]

        for i in range(len(y)):
            equation = 1
            for j in range(len(x)):
                if i != j:
                    equation = equation * (pitch - x[j]) / (x[i] - x[j])
            equation_result = equation_result + equation * y[i]
        return equation_result

    def select_note(self):
        legal_note = False
        while not legal_note:
            self.target_note = input('Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n').upper()
            if self.target_note not in self.frequencies:
                print("Illegal note, please try again...")
            else:
                legal_note = True
