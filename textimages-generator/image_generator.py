from PIL import Image, ImageDraw, ImageFont
import random
import os
import csv

class ImageGenerator:
    def __init__(self, font_folder="fonts", output_folder="images", image_dimensions=(500, 500), font_size=24,
                 font_color=(255, 255, 255)):
        self.output_folder = output_folder
        self.font_folder = font_folder
        self.image_dimensions = image_dimensions
        self.font_list = os.listdir(font_folder)
        self.font_size = font_size
        self.font_color = font_color
        self.initialize_dictionary()

    def build_folders(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.font_folder):
            os.makedirs(self.font_folder)

    def generate_images(self, count_words_with_accents, count_words_without_diacritics):
        
        for _ in range(count_words_with_accents):
            random_word = random.choice(self.words_with_accent)
            self.generate_new_image(random_word)

        for _ in range(count_words_without_diacritics):
            random_word = random.choice(self.words_without_diacritics)
            self.generate_new_image(random_word)

    def generate_new_image(self, text):

        font_path = "fonts/"+random.choice(self.font_list)        
        font = ImageFont.truetype(font_path, random.randint(20, 40))
        image = Image.new("RGB", (self.image_dimensions[0], self.image_dimensions[1]), self.font_color)
        draw = ImageDraw.Draw(image)

        position = (10, 10)

        draw.text(position, text, fill="black", font=font)

        image.save(self.output_folder+"/"+text+".tiff")

    def initialize_dictionary(self):
        with open("dictionary.csv", "r", encoding="utf-8") as file:
            fr_dict = [word[0] for word in csv.reader(file)]

        def contains_accent(word):
            return any(accent in word for accent in ['è', 'é', 'ê'])
        
        #Separate lists for words with the accents we want to detect and another one for all words without diacritics.
        self.words_with_accent = [word for word in fr_dict if contains_accent(word)]
        self.words_without_diacritics = [word for word in fr_dict if not contains_accent(word)]


        #TODO add graining, set image settings, define bounding boxes