from PIL import Image, ImageDraw, ImageFont
from bounding_box_generator import BboxGenerator
import random
import os
import csv

class ImageGenerator:
    def __init__(self, font_folder="fonts", output_folder="images", image_dimensions=(1000, 200),
                 font_color=(255, 255, 255), maximum_noise_level = 150):
        self.output_folder = output_folder
        self.font_folder = font_folder
        self.image_dimensions = image_dimensions
        self.font_list = os.listdir(font_folder)
        self.font_color = font_color
        self.maximum_noise_level = maximum_noise_level
        self.initialize_dictionary()

    def build_folders(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.font_folder):
            os.makedirs(self.font_folder)

    def generate_images(self, count_words_with_accents, count_words_without_diacritics):
        
        for _ in range(count_words_with_accents):
            random_word = random.choice(self.words_with_diacritics)
            self.words_with_diacritics.remove(random_word)
            self.generate_new_image(random_word)

        for _ in range(count_words_without_diacritics):
            random_word = random.choice(self.words_without_diacritics)
            self.words_without_diacritics.remove(random_word)
            self.generate_new_image(random_word)

    def generate_new_image(self, text):

        bbox_generator = BboxGenerator()

        font_path = "fonts/" + random.choice(self.font_list)        
        font = ImageFont.truetype(font_path, random.randint(40, 80))
        image = Image.new("RGB", (self.image_dimensions[0], self.image_dimensions[1]), self.font_color).convert('L')
        draw = ImageDraw.Draw(image)

        position = (5, 5)

        draw.text(position, text, fill="black", font=font)

        print(text)

        for index, char in enumerate(text):
            if(self.contains_diacritics(char)):
                bbox_generator.draw_bounding_box(font, image, draw, text[:index], char)

        #image = self.add_noise(image, random.randint(0, self.maximum_noise_level) / 300)

        #image = image.convert("1")

        #image.save(self.output_folder+"/"+text+".tiff", compression="group4")
        image.save(self.output_folder+"/"+text+".tiff")

    def initialize_dictionary(self):
        #Dictionary source: https://github.com/hbenbel/French-Dictionary/tree/master
        with open("dictionary.csv", "r", encoding="utf-8") as file:
            fr_dict = [word[0] for word in csv.reader(file)]

        
        #Separate lists for words with the accents we want to detect and another one for all words without diacritics.
        self.words_with_diacritics = [word for word in fr_dict if self.contains_diacritics(word)]
        self.words_without_diacritics = [word for word in fr_dict if not self.contains_diacritics(word)]

    def contains_diacritics(self, word):
        return any(accent in word for accent in  ['á', 'à', 'â', 'é', 'è', 'ê', 'î', 'ô', 'û', 'ŷ'])
    
    def add_noise(self, image, noise_factor ):
        width, height = image.size
        grain = Image.new('L', (width, height))

        for x in range(width):
            for y in range(height):
                grain_level_adjusted = int(random.uniform(-255 * noise_factor, 255 * noise_factor))
                pixel_value = image.getpixel((x, y))
                new_pixel_value = max(0, min(255, pixel_value + grain_level_adjusted))
                grain.putpixel((x, y), new_pixel_value)

        return Image.blend(image, grain.convert('L'), alpha=noise_factor)