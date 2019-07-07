import pyaudio
import wave
from threading import Thread
from time import sleep
import os


class Audio:
    def __init__(self, audio_length):
        self.audio_length = audio_length

        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.samples_per_second = 44100
        self.seconds = 5
        self.filename = "audio_record_1"
        self.p = ''
        self.stream = ''
        self.frames_list = []
        self.counter = 1
        self.user_path = os.path.expanduser('~\\documents')
        self.test_dir = os.path.expanduser('~/')

    def handle_audio(self):
        while len(os.listdir(f'{self.test_dir}/audio_record'))*self.seconds < self.audio_length:
            self.filename = f'{self.filename[:-1]}{self.counter}'

            self.init_stream()
            self.grab_audio()
            self.stop_recording()
            self.save_to_file()

            self.counter += 1

    def init_stream(self):
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.samples_per_second,
                        frames_per_buffer=self.chunk,
                        input=True)

    def grab_audio(self):
        for i in range(0, int(self.samples_per_second / self.chunk * self.seconds)):
            data = self.stream.read(self.chunk)
            self.frames_list.append(data)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def save_to_file(self):

        if not os.path.isdir(f'{self.test_dir}/audio_record'):
            os.mkdir(f'{self.test_dir}/audio_record')

        path =  f'{self.test_dir}/audio_record/{self.filename}.wav'

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.samples_per_second)
        wf.writeframes(b''.join(self.frames_list))
        wf.close()

        self.cleanup()

    def cleanup(self):
        self.frames_list = []
        self.stream = ''
        self.p = ''


if __name__ == '__main__':
    aud = Audio(20)
    aud.handle_audio()