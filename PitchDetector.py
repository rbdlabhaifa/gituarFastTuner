import os
import copy
import time
import numpy as np
import scipy.fftpack
import sounddevice as sd


class PitchDetector:
    def __init__(self, notes, octave_bands, iterations):

        self.notes = notes
        self.octave_bands = octave_bands
        self.iterations = 0
        self.max_iterations = iterations

        self.recent_pitch = 440  # defining a1
        self.detected_pitches = []

        self.sample_frequency = 48000  # sample frequency in Hz
        self.sample_length = 1 / self.sample_frequency  # length between two samples in seconds

        self.window_size = 48000  # window size of the DFT in samples
        self.window_step = 12000  # step size of window
        self.window_length = self.window_size / self.sample_frequency  # length of the window in seconds
        self.hanning_window = np.hanning(self.window_size)
        self.window_samples = [0 for _ in range(self.window_size)]
        self.note_buffer = ["1", "2"]

        self.delta_frequency = self.sample_frequency / self.window_size  # frequency step width of the interpolated DFT

        self.max_hps = 5  # max number of harmonic product spectrum
        self.tuning_threshold = 1e-6  # tuning is activated if the signal power exceeds this threshold
        self.white_noise = 0.2  # everything under WHITE_NOISE_THRESH * avg_energy_per_freq is cut off

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
        i = int(np.round(np.log2(pitch / self.recent_pitch) * notes_count))
        closest_note = self.notes[i % notes_count] + str(notes_count // 3 + (i + notes_count // 4) // notes_count)
        closest_pitch = self.recent_pitch * 2 ** (i / notes_count)
        return closest_note, closest_pitch

    def callback(self, data, frames, time, status):
        """
      Callback function of the InputStream method.
      That's where the magic happens ;)
      """
        if any(data):
            self.window_samples = np.concatenate((self.window_samples, data[:, 0]))  # append new samples
            self.window_samples = self.window_samples[len(data[:, 0]):]  # remove old samples

            # skip if signal power is too low
            signal_power = (np.linalg.norm(self.window_samples, ord=2, axis=0) ** 2) / len(self.window_samples)
            if signal_power < self.tuning_threshold:
                os.system('cls' if os.name == 'nt' else 'clear')
                return

            # avoid spectral leakage by multiplying the signal with a hanning window
            hanning_samples = self.window_samples * self.hanning_window
            magnitude_spec = abs(scipy.fftpack.fft(hanning_samples)[:len(hanning_samples) // 2])

            # supress mains hum, set everything below 62Hz to zero
            for i in range(int(62 / self.delta_frequency)):
                magnitude_spec[i] = 0

            # calculate average energy per frequency for the octave bands
            # and suppress everything below it
            for j in range(len(self.octave_bands) - 1):
                ind_start = int(self.octave_bands[j] / self.delta_frequency)
                ind_end = int(self.octave_bands[j + 1] / self.delta_frequency)
                ind_end = ind_end if len(magnitude_spec) > ind_end else len(magnitude_spec)
                avg_energy_per_freq = (np.linalg.norm(magnitude_spec[ind_start:ind_end], ord=2, axis=0) ** 2) / (
                        ind_end - ind_start)
                avg_energy_per_freq **= 0.5
                for i in range(ind_start, ind_end):
                    magnitude_spec[i] = magnitude_spec[i] if magnitude_spec[
                                                                 i] > self.white_noise * avg_energy_per_freq else 0

            # interpolate spectrum
            mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1 / self.max_hps),
                                      np.arange(0, len(magnitude_spec)), magnitude_spec)
            mag_spec_ipol = mag_spec_ipol / np.linalg.norm(mag_spec_ipol, ord=2, axis=0)  # normalize it

            hps_spec = copy.deepcopy(mag_spec_ipol)

            # calculate the HPS
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

            os.system('cls' if os.name == 'nt' else 'clear')
            if self.note_buffer.count(self.note_buffer[0]) == len(self.note_buffer):
                self.detected_pitches.append(max_freq)
                self.recent_pitch = max_freq
                self.iterations += 1

    def detect(self):
        try:
            input_stream = sd.InputStream(channels=1, callback=self.callback, blocksize=self.window_step,
                                          samplerate=self.sample_frequency)
            print(f"Collecting samples...")
            print("---------------------- PLAY ----------------------")
            input_stream.start()
            while self.iterations < self.max_iterations:
                time.sleep(0.5)
            input_stream.stop()
            input_stream.close()
            print(f"\nCollected samples, evaluating...\n")
            return max(set(self.detected_pitches), key=self.detected_pitches.count)
        except Exception as e:
            print(f"Caught exception: {e}")
