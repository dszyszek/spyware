import os
import img2pdf
from mss import mss
from time import sleep
import pyscreenshot as ImageGrab

from normalize_path import normalize_path_name


class Visual:
    def __init__(self, screenshot_period, user_path, frequency):
        self.screenshot_period = screenshot_period
        self.user_path = user_path
        self.screenshot_state = True
        self.frequency = frequency

    def make_pdf(self):
        listed_dir = os.listdir(normalize_path_name(self.user_path, 'images_record'))
        images_with_location = [normalize_path_name(self.user_path, 'images_record', a) for a in listed_dir]

        with open(normalize_path_name(self.user_path, 'pdf_record', 'ready.pdf'), 'wb') as output_pdf:
            pdf_bytes = img2pdf.convert(images_with_location)

            output_pdf.write(pdf_bytes)

        for x in images_with_location:
            try:
                os.remove(x)
            except:
                pass

    def make_screenshot(self):
        sct = mss()
        counter = 0

        images_record_dir_list = os.listdir(normalize_path_name(self.user_path, 'images_record'))

        while len(images_record_dir_list)*self.screenshot_period <= self.frequency:
            images_record_dir_list = os.listdir(normalize_path_name(self.user_path, 'images_record'))

            counter += 1
            sleep(self.screenshot_period)

            im = ImageGrab.grab()
            im.save(normalize_path_name(self.user_path, 'images_record', f'image{counter}.png'))


if __name__ == '__main__':
    vsl = Visual(5, normalize_path_name(os.path.expanduser('~'), 'documents'), 30)
    vsl.make_screenshot()