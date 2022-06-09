from sounddevice import InputStream
from scipy.fftpack import fft
from os import system, name
from copy import deepcopy
from time import sleep
import numpy as np


class PitchDetector:
    def __init__(self, notes, octave_bands, iterations):
        self.notes = notes
        self.octave_bands = octave_bands
        self.iterations = 0
        self.max_iterations = iterations

        self.base_pitch = 440  # defining a4
        self.base_octave = 4  # defining a4
        self.detected_pitches = []

        self.sample_frequency = 48000  # sample frequency in Hz
        self.sample_length = 1 / self.sample_frequency  # length between two samples in seconds

        self.window_size = 48000  # window size of the DFT in samples
        self.window_step = 12000  # step size of window
        self.window_length = self.window_size / self.sample_frequency  # length of the window in seconds
        self.hanning_window = np.hanning(self.window_size)
        self.window_samples = [0 for _ in range(self.window_size)]
        self.note_buffer = ["1", "2"]  # saves the last 2 notes, and only registers the new note if it is equal to the previous
        self.delta_frequency = self.sample_frequency / self.window_size  # frequency step width of the interpolated DFT

        self.max_hps = 5  # max number of harmonic product spectrum
        self.tuning_threshold = 1e-6  # tuning is activated if the signal power exceeds this threshold

    def find_closest_note(self, pitch):
        """
        This function finds the closest note for a given pitch
        Parameters:
            pitch (float): pitch given in hertz
        Returns:
            closest_note (str): e.g. a, g#, ..
            closest_pitch (float): pitch of the closest note in hertz
        """
        notes_count = len(self.notes)
        note_index = int(np.round(np.log2(pitch / self.base_pitch) * notes_count))
        closest_note = self.notes[note_index % notes_count] + str(
            self.base_octave + (note_index + 9) // notes_count)
        closest_pitch = self.base_pitch * 2 ** (note_index / notes_count)
        return closest_note, closest_pitch

    def callback(self, data, frames, time, status):
        """
        Callback function of the InputStream method.
        This is where the magic happens ;)
        """
        if any(data):
            self.window_samples = np.concatenate((self.window_samples, data[:, 0]))  # append new samples
            self.window_samples = self.window_samples[len(data[:, 0]):]  # remove old samples

            # skip if signal power is too low
            signal_power = (np.linalg.norm(self.window_samples, ord=2, axis=0) ** 2) / len(self.window_samples)
            if signal_power < self.tuning_threshold:
                system('cls' if name == 'nt' else 'clear')
                return

            # avoid spectral leakage by multiplying the signal with a hanning window
            hanning_samples = self.window_samples * self.hanning_window
            magnitude_spec = abs(fft(hanning_samples)[:len(hanning_samples) // 2])

            # supress mains hum, set everything below 62Hz to zero
            for i in range(int(60 / self.delta_frequency)):
                magnitude_spec[i] = 0

            # Here the DFT spectrum is interpolated. We need to do this as we are required to down sample the spectrum
            # in the latter steps. Imagine there is a perfect peak at a given frequency and all the frequencies next to
            # it are zero. If we now down sample the spectrum, there is a certain risk that this peak is simply ignored.
            # This can be avoided having an interpolated spectrum as the peaks are "smeared" over a larger area.
            mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / self.max_hps),
                                      np.arange(0, len(magnitude_spec)), magnitude_spec)
            mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2, axis=0)  # normalize it

            hps_spec = deepcopy(mag_spec_ipol)

            # calculate the HPS and stop if spectrum is completely 0
            for i in range(self.max_hps):
                tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(mag_spec_ipol) / (i + 1)))],
                                           mag_spec_ipol[::(i + 1)])
                if not any(tmp_hps_spec):
                    break
                hps_spec = tmp_hps_spec

            max_ind = np.argmax(hps_spec)
            max_freq = max_ind * (self.sample_frequency / self.window_size) / self.max_hps

            closest_note, closest_pitch = self.find_closest_note(max_freq)
            max_freq = round(max_freq, 1)
            closest_pitch = round(closest_pitch, 1)

            self.note_buffer.insert(0, closest_note)  # note that this is a ringbuffer
            self.note_buffer.pop()
            # Only print the note, if the previous note is the same.
            if self.note_buffer.count(self.note_buffer[0]) == len(self.note_buffer):
                self.detected_pitches.append(max_freq)
                print(f"Closest note: {closest_note} {max_freq}/{closest_pitch}")
                self.iterations += 1

    def detect(self):
        try:
            input_stream = InputStream(channels=1, callback=self.callback, blocksize=self.window_step,
                                       samplerate=self.sample_frequency)
            print(f"Collecting samples...")
            print("---------------------- PLAY ----------------------")
            input_stream.start()
            while self.iterations < self.max_iterations:
                sleep(0.5)
            input_stream.stop()
            input_stream.close()
            print(f"\nCollected samples, evaluating...\n")
            print(f"pitches: {self.detected_pitches}")
            return max(set(self.detected_pitches), key=self.detected_pitches.count)
        except Exception as e:
            print(f"Caught exception: {e}")
