from PIL import Image, ImageDraw, ImageFont
import random
import os


class ImageGenerator:
    def __init__(self, font_folder="fonts", output_folder="images", image_dimensions=(500, 500), font_size=24,
                 font_color=(255, 255, 255)):
        self.output_folder = output_folder
        self.font_folder = font_folder
        self.image_dimensions = image_dimensions
        self.font_list = os.listdir(font_folder)
        self.font_size = font_size
        self.font_color = font_color

    def build_folders(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.font_folder):
            os.makedirs(self.font_folder)

    def generate_new_image(self):
        font = ImageFont.truetype(random.choice(self.font_list), random.randint(20, 40))
        non_diacritic_text = textlist
        diacritic_text = diacritic_text_list
        Image.new("RGB", (self.image_dimensions[0], self.image_dimensions[1]), self.font_color)
