import os
from PIL import Image
import json

class ImageProcessor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def process_image(self, size):
        with os.scandir(self.input_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    if entry.name[-3:] == 'jpg':
                        img = Image.open(entry)
                        img=img.resize((128, 128))
                        img=img.convert('L')
                        img.save(os.path.join(self.output_dir, entry.name))

with open('config.json') as config_file:
    config = json.load(config_file)

processor = ImageProcessor(config['input_dir'], config['output_dir'])