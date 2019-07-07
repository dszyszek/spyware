import pyaudio
import wave


class Audio:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.samples_per_second = 44100
        self.seconds = 3
        self.filename = "audio_record.wav"
        self.p = ''
        self.stream = ''
        self.frames_list = []

    def init_stream(self):
        self.p = pyaudio.PyAudio()

        self.stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.samples_per_second,
                        frames_per_buffer=self.chunk,
                        input=True)

    def grab_audio(self):
        for i in range(0, int(self.samples_per_second / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            self.frames_list.append(data)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def save_to_file(self):
        path = os.path.expanduser('~\\documents') + '\\' + self.filename

        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.samples_per_second)
        wf.writeframes(b''.join(self.frames_list))
        wf.close()