from PIL import Image, ImageDraw, ImageFont
import random
import os


class ImageGenerator:
    def __init__(self, font_path=".", output_folder=".", image_width=500, image_height=500, font_size=24, font_color="BLACK"):
        self.output_folder = output_folder
        self.image_width = image_width
        self.image_height = image_height
        self.font_list = os.listdir(font_path)
        self.font_size = font_size
        self.font_color = font_color

    def generate(self):
        return self.font_list



