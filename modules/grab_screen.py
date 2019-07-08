import os
import img2pdf
from mss import mss
from time import sleep
import pyscreenshot as ImageGrab
from PIL import Image

from modules.normalize_path import normalize_path_name


class Visual:
    def __init__(self, screenshot_period, user_path, frequency):
        self.screenshot_period = screenshot_period
        self.user_path = user_path
        self.screenshot_state = True
        self.frequency = frequency
        self.counter = 1

    def make_pdf(self):
        listed_dir = os.listdir(normalize_path_name(self.user_path, 'images_record'))
        images_with_location = [normalize_path_name(self.user_path, 'images_record', a) for a in listed_dir][:-1]

        with open(normalize_path_name(self.user_path, 'pdf_record', f'ready_{self.counter}.pdf'), 'wb') as output_pdf:
            if images_with_location:
                pdf_bytes = img2pdf.convert(images_with_location)

                output_pdf.write(pdf_bytes)

                self.counter += 1

        for x in images_with_location:
            try:
                os.remove(x)
            except:
                pass

    def make_screenshot(self):
        sct = mss()
        counter = 0

        images_record_dir_list = os.listdir(normalize_path_name(self.user_path, 'images_record'))

        while len(images_record_dir_list)*self.screenshot_period <= int(self.frequency):
            images_record_dir_list = os.listdir(normalize_path_name(self.user_path, 'images_record'))

            counter += 1
            sleep(self.screenshot_period)

            im = ImageGrab.grab()
            im.save(normalize_path_name(self.user_path, 'images_record', f'image{counter}.png'))

    def remove_alpha_channel(self):
        images_dir = normalize_path_name(self.user_path, 'images_record')

        for root, subfolders, files in os.walk(images_dir):
            for file in files:
                try:
                    image = Image.open(os.path.join(images_dir, root, file))
                    if image.mode == 'RGBA':
                        bg = Image.new('RGB', image.size, (255, 255, 255))
                        bg.paste(image, (0, 0), image)
                        bg.save(os.path.join(images_dir, root, file), "PNG")
                except:
                    pass


if __name__ == '__main__':
    vsl = Visual(5, normalize_path_name(os.path.expanduser('~'), 'documents'), 30)
    vsl.make_screenshot()