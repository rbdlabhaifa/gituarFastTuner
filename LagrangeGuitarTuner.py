import json
from PitchDetector import PitchDetector
from AuxiliaryFunctions import countdown

from ConfigSections import *


class LagrangeGuitarTuner:
    def __init__(self):
        self.iterations = 0
        self.frequencies = {"E4": 329.63, "B3": 246.94, "G3": 196.00, "D3": 146.83, "A2": 110.00, "E2": 82.41}
        self.octave_bands = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
        self.notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        self.samples = {'E2': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5], [45, 54, 62.5, 70.5, 77.5, 84.2, 90.3, 96]],
                        'A2': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], [52.2, 58.2, 69, 77.9, 86.8, 94, 102, 108.1, 115.1]],
                        'D3': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5], [56, 66,
                         77, 86.5, 96.5, 104.4, 113, 120, 128.2, 134.7, 141.5, 147, 154, 159.8, 165.5, 170.1, 175, 179, 183.5,187.1]],
                        'G3': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5],
                               [70.5, 81.3, 94.2, 105.5, 117.1, 126.3, 136, 144, 152.7, 160, 167.7, 174.6, 182, 188.2,
                                195, 200.5, 207, 211.4,216.5, 220.5, 225, 229, 233.3, 236.7]],
                        'B3': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5],
                               [96.7, 115, 138, 157, 176, 190, 210, 223, 239.3, 251.5, 265.5, 276.7]],
                        'E4': [[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5],
                               [158.8, 172.5, 194.3, 211.3, 230, 245.7, 261.5, 275, 290, 302.2, 315.8, 326.5, 338.5, 348, 359, 367.3]]
                        }
        self.target_note = ''

    def detect_pitch(self):
        pitch_detector = PitchDetector(self.notes, self.octave_bands, 13)
        detected_pitch = pitch_detector.detect()
        return detected_pitch

    def is_tuned(self, distance_to_pitch):
        if -2 < distance_to_pitch < 2:
            print(f"{self.target_note} is tuned.")
            return True
        return False

    def get_instructions(self, current_pitch, target_pitch):
        lagrange_target = self.lagrange_interpolation(target_pitch)
        lagrange_current = self.lagrange_interpolation(current_pitch)
        return lagrange_current, lagrange_target

    def print_instructions(self, distance_to_pitch):
        degrees_to_pitch = round(distance_to_pitch * 360)
        half_turns_to_pitch = round(degrees_to_pitch/180)
        turns_to_pitch = half_turns_to_pitch/2
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
        countdown(5)
        current_pitch = self.detect_pitch()
        print(f"First detected pitch: {current_pitch}")

        distance_to_pitch = target_pitch - current_pitch
        if self.is_tuned(distance_to_pitch):
            # The note is already tuned
            return

        current_turns, target_turns = self.get_instructions(current_pitch, target_pitch)
        self.print_instructions(target_turns - current_turns)
        print("Going again in", end=' ')
        previous_turns = current_turns
        countdown(20)
        current_pitch = self.detect_pitch()

        while not self.is_tuned(target_pitch - current_pitch) and self.iterations < 3:
            print(f"new detected pitch: {current_pitch}")
            current_turns, target_turns = self.get_instructions(current_pitch, target_pitch)
            print(f"current_turns: {current_turns}")
            print(f"targert_turns: {target_turns}")
            off_percentage = (current_turns - previous_turns) / (target_turns - previous_turns)
            print(f"off_percentage: {off_percentage}")
            self.print_instructions(target_turns - current_turns)
            previous_turns = current_turns
            print("Going again in", end=' ')
            self.iterations += 1
            countdown(20)
            current_pitch = self.detect_pitch()
        if self.is_tuned(target_pitch - current_pitch):
            return
        else:
            print(f"new detected pitch: {current_pitch}")
            return




        # second_detected_pitch = self.detect_pitch()
        # print(f"Second detected pitch: {second_detected_pitch}")
        #
        # if not self.is_tuned(target_pitch - second_detected_pitch):
        #     # Need to adjust the frequency changes
        #     second_turns, target_turns = self.get_instructions(second_detected_pitch, target_pitch)
        #     print (f"second_turns: {second_turns}")
        #     print (f"targer_turns: {target_turns}")
        #     off_percentage = (second_turns - first_turns) / (target_turns - first_turns)
        #     print(f"off_percentage: {off_percentage}")
        #     self.print_instructions((target_turns - second_turns) * (1 + 1/off_percentage))
        #     print("Going again in", end=' ')
        #     countdown(20)
        # else:
        #     return
        #
        # third_detected_pitch = self.detect_pitch()
        # print(f"third detected pitch: {third_detected_pitch}")
        #
        # if not self.is_tuned(target_pitch - third_detected_pitch):
        #     # Need to adjust the frequency changes
        #     third_turns, target_turns = self.get_instructions(third_detected_pitch, target_pitch)
        #     print (f"second_turns: {third_turns}")
        #     print (f"targer_turns: {target_turns}")
        #     off_percentage = (third_turns - second_turns) / (target_turns - second_turns)
        #     print(f"off_percentage: {off_percentage}")
        #     self.print_instructions(target_turns - third_turns)
        #     print("Going again in", end=' ')
        #     countdown(20)
        # else:
        #     return
        #
        # forth_detected_pitch = self.detect_pitch()
        # print(f"forth detected pitch: {forth_detected_pitch}")
        # if not self.is_tuned(target_pitch - forth_detected_pitch):
        #     # Need to adjust the frequency changes
        #     forth_turns, target_turns = self.get_instructions(forth_detected_pitch, target_pitch)
        #     print (f"second_turns: {forth_turns}")
        #     print (f"targer_turns: {target_turns}")
        #     off_percentage = (forth_turns - third_turns) / (target_turns - third_turns)
        #     print(f"off_percentage: {off_percentage}")
        #     self.print_instructions(target_turns - forth_turns)
        #     print("Going again in", end=' ')
        #     countdown(20)
        #     last_detected_pitch = self.detect_pitch()
        #     print(f"last detected pitch: {last_detected_pitch}")
        # else:
        #     return

    def lagrange_interpolation(self, pitch):
        equation_result = 0
        current_samples = self.samples[self.target_note]
        for i in range(len(current_samples[1])):
            equation = 1
            for j in range(len(current_samples[1])):
                if i != j:
                    equation = equation * (pitch - current_samples[1][j]) / (current_samples[1][i] - current_samples[1][j])
            equation_result = equation_result + equation * current_samples[0][i]
        return equation_result

    def select_note(self):
        legal_note = False
        while not legal_note:
            self.target_note = input('Please select note you which to tune to: E4, B3, G3, D3, A2, E2\n').upper()
            if self.target_note not in self.frequencies:
                print("Illegal note, please try again...")
            else:
                legal_note = True
