from PIL import Image, ImageDraw, ImageFont
from bounding_box_generator import BboxGenerator
import random
import os
import csv

class ImageGenerator:
    def __init__(self, font_folder="fonts", output_folder="images",
                 font_color=(255, 255, 255)):
        self.output_folder = output_folder
        self.font_folder = font_folder
        self.font_list = os.listdir(font_folder)
        self.font_color = font_color
        self.initialize_dictionary()

    def build_folders(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.font_folder):
            os.makedirs(self.font_folder)

    def generate_images(self, count_words_with_accents, count_words_without_diacritics, maximum_noise_level):
        
        self.maximum_noise_level = maximum_noise_level

        for _ in range(count_words_with_accents):
            random_word = random.choice(self.words_with_diacritics)
            if(len(random_word) > 30):
                continue
            self.words_with_diacritics.remove(random_word)
            self.generate_new_image(random_word)

        for _ in range(count_words_without_diacritics):
            random_word = random.choice(self.words_without_diacritics)
            if(len(random_word) > 30):
                continue
            self.words_without_diacritics.remove(random_word)
            self.generate_new_image(random_word)

    def generate_new_image(self, text):


        bbox_generator = BboxGenerator()

        font_path = "fonts/" + random.choice(self.font_list)        
        font = ImageFont.truetype(font_path, random.randint(40, 80))

        ascent, descent = font.getmetrics()
        text_width = font.getmask(text).getbbox()[2]
        text_height = font.getmask(text).getbbox()[3] + descent

        self.image_dimensions = (text_width + 10, text_height + 15)
        image = Image.new("RGB", (self.image_dimensions[0] + 10, self.image_dimensions[1]), self.font_color).convert('L')
        draw = ImageDraw.Draw(image)

        position = (5, 2)

        draw.text(position, text, fill="black", font=font)

        print(text)

        bounding_boxes = []

        for index, char in enumerate(text):
            if(self.contains_diacritics(char)):
                bounding_boxes.append(bbox_generator.generate_bounding_box(font, image, draw, text[:index], char))

        for (character_class,  bounding_box) in bounding_boxes:
            self.write_to_yolo_text_file(character_class, bounding_box, text)

        image = self.add_noise(image, random.randint(0, self.maximum_noise_level) / 300)

        image = image.convert("1")

        image.save(self.output_folder+"/"+text+".tiff", compression="group4")
        
    def write_to_yolo_text_file(self, character_class, bbox_accent_adjusted, text):
        width_in_pixels = bbox_accent_adjusted[2] - bbox_accent_adjusted[0]
        height_in_pixels = bbox_accent_adjusted[3] - bbox_accent_adjusted[1]
        x_center_in_pixels = bbox_accent_adjusted[0] + width_in_pixels / 2
        y_center_in_pixels = bbox_accent_adjusted[1] + height_in_pixels / 2

        width_normalised = width_in_pixels / self.image_dimensions[0]
        height_normalised = height_in_pixels / self.image_dimensions[1]
        x_center_normalised = x_center_in_pixels / self.image_dimensions[0]
        y_center_normalised = y_center_in_pixels / self.image_dimensions[1]

        with open(self.output_folder + '/' + text + '.txt', 'a') as file:
            file.writelines("%d %f %f %f %f \n" % (character_class, x_center_normalised, y_center_normalised, width_normalised, height_normalised))
    
    def initialize_dictionary(self):
        #Dictionary source: https://github.com/hbenbel/French-Dictionary/tree/master
        with open("dictionary.csv", "r", encoding="utf-8") as file:
            fr_dict = [word[0] for word in csv.reader(file)]

        
        #Separate lists for words with the accents we want to detect and another one for all words without diacritics.
        self.words_with_diacritics = [word for word in fr_dict if self.contains_diacritics(word)]
        self.words_without_diacritics = [word for word in fr_dict if not self.contains_diacritics(word)]

    def contains_diacritics(self, word):
        return any(accent in word for accent in  ['á', 'à', 'â', 'é', 'è', 'ê', 'ô', 'û', 'ŷ'])
    
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