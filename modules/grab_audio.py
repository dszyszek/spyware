import pyaudio
import wave
from threading import Thread
from time import sleep
import os
from random import randint

from normalize_path import normalize_path_name


class Audio:
    def __init__(self, audio_length):
        self.audio_length = audio_length

        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.samples_per_second = 44100
        self.seconds = 5
        self.filename = "audio_record"
        self.counter = 1
        self.user_path = normalize_path_name(os.path.expanduser('~'), 'documents')

    def handle_audio(self):
        if not os.path.isdir(normalize_path_name(self.user_path, 'audio_record')):
            os.mkdir(normalize_path_name(self.user_path, 'audio_record'))

        normalized_dir = normalize_path_name(self.user_path, 'audio_record')

        while len(os.listdir(normalized_dir))*self.seconds <= self.audio_length:
            filename = self.filename + str(self.counter)
            self.record(filename)

            self.counter += 1

    def record(self, name):
        frames_list = []
        random_number = self.get_random_number()

        p = pyaudio.PyAudio()
        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.samples_per_second,
                        frames_per_buffer=self.chunk,
                        input=True)

        for i in range(0, int(self.samples_per_second / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames_list.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()


        normalized_audio_dir = normalize_path_name(self.user_path, 'audio_record')
        path =  normalize_path_name(normalized_audio_dir, f'{random_number}_{name}.wav')

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.samples_per_second)
        wf.writeframes(b''.join(frames_list))
        wf.close()

    def get_random_number(self):
        random_number = str(randint(0, 20))

        for n in range(0, 10):
            random_number += str(randint(0, 20))
        return random_number

if __name__ == '__main__':
    aud = Audio(170)
    aud.handle_audio()