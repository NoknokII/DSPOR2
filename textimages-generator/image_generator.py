from PIL import Image, ImageDraw, ImageFont, ImageFilter
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

    def generate_images(self, count_words_with_accents, count_words_without_diacritics, maximum_noise_level, maximum_scanning_lines, scanning_line_probability):
        
        self.maximum_noise_level = maximum_noise_level
        self.maximum_scanning_lines = maximum_scanning_lines
        self.scanning_line_probability = scanning_line_probability


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

        _, descent = font.getmetrics()
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

        image = self.add_noise(image, self.maximum_noise_level)

        image = self.simulate_scanning_artifacts(image)

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
        self.words_with_diacritics = [word for word in fr_dict if self.contains_diacritics(word) and not self.has_multiple_words(word)]
        self.words_without_diacritics = [word for word in fr_dict if not self.contains_diacritics(word) and not self.has_multiple_words(word)]

    def contains_diacritics(self, word):
        return any(accent in word for accent in  ['á', 'à', 'â', 'é', 'è', 'ê', 'ô', 'û', 'ŷ'])
    
    def has_multiple_words(self, input_string):
        space_count = input_string.count(' ')
        return space_count >= 1
    
    def add_noise(self, image, noise_factor ):
        draw = ImageDraw.Draw(image)
        width, height = image.size
        for y in range(height):
            for x in range(width):
                if random.random() < 0.00001 * noise_factor:
                    splotch_size = random.randint(2, 10)
                    splotch_color = random.randint(0, 50)
                    # Random eccentricity
                    eccentricity = random.uniform(0.3, 1.0)
                    # Random rotation
                    rotation = random.uniform(0, 360)
                    # Calculate bounding box
                    bbox = (x - splotch_size, y - int(splotch_size * eccentricity), 
                            x + splotch_size, y + int(splotch_size * eccentricity))
                    # Draw ellipse
                    draw.ellipse(bbox, fill=splotch_color, outline=None)
        return image
    
    def simulate_scanning_artifacts(self, image):
        num_lines_affected = random.randint(0, self.maximum_scanning_lines)

        image = image.filter(ImageFilter.GaussianBlur(radius=random.randint(0, 1)))

        draw = ImageDraw.Draw(image)
        width, height = image.size
        num_lines = random.randint(5, 10)
        for _ in range(num_lines):
            y = random.randint(0, height)
            if num_lines_affected > 0 and random.random() < self.scanning_line_probability:
                line_fill = random.randint(200, 255)
                draw.line((0, y, width, y), fill=line_fill, width=random.randint(1, 3))

                # Introduce noise in the lines
                line_noise = random.randint(0, 20)
                for x in range(width):
                    if random.random() < 0.5:
                        draw.point((x, y), fill=min(255, line_fill + random.randint(-line_noise, line_noise)))
                num_lines_affected -= 1

        return image
