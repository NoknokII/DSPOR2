import cv2 as cv
import numpy as np
from PIL import ImageDraw
import math


class BboxGenerator:
    def generate_bounding_box(self, font, image, text_until_current_char, current_character, offset_x):
        bbox = []
        #Min size 10 avoids single pixels detected as diacritic
        cc_dict = self.cc_analyse(image,10,10000)
        current_character_coordinates = offset_x+font.getlength(text_until_current_char)
        current_character_width = font.getlength(current_character)
        w,h = image.size

        cc_dict.sort(key=lambda cc: self.distance(cc['center_point_x'], cc['center_point_y'], current_character_coordinates + current_character_width//2 , 0),
                         reverse=False)


        character_class = self.retrieve_class(current_character)
        bbox.append((cc_dict[0]['x']+ (cc_dict[0]['width'] / 2)) / w)
        bbox.append((cc_dict[0]['y']+ (cc_dict[0]['height'] / 2)) / h)
        bbox.append((cc_dict[0]['width']+2) / w)
        bbox.append((cc_dict[0]['height']+2) / h)
        return character_class, bbox
        

                
    def retrieve_base_character(self, current_character):
        match current_character:
            case 'á' | 'à' | 'â':
                return 'a'
            case 'é' | 'è' | 'ê':
                return 'e'
            case 'î':
                return 'i'
            case 'ô':
                return 'o'
            case 'û':
                return 'u'
            case 'ŷ':
                return 'y'
            
    def retrieve_class(self, current_character):
        match current_character:
            case 'á' | 'é':
                return 0
            case 'à' | 'è':
                return 1
            case 'â'| 'ê'| 'î' | 'ô' | 'û' | 'ŷ':
                return 2

    def draw_line_on_image(self,img, output_path, start_point, end_point, color=(255, 0, 0), line_width=2):
        # Open the image
        img2 =  img.copy()
        img2 = img2.convert("RGB")
        # Create a drawing object
        draw = ImageDraw.Draw(img2)

        # Draw a line on the image
        draw.line([start_point, end_point], fill=color, width=line_width)

        # Save the modified image
        img2.save(output_path)

    def draw_rect_on_image(self,img, output_path, start_point, end_point, color=(255, 0, 0), line_width=2):
        # Open the image
        img2 =  img.copy()
        img2 = img2.convert("RGB")
        # Create a drawing object
        draw = ImageDraw.Draw(img2)

        # Draw a line on the image
        draw.rectangle((start_point,end_point), outline=color)

        # Save the modified image
        img2.save(output_path)

    def cc_analyse(self, image, min_size, max_size):
        image = np.array(image)
        image = image.astype(float)
        image = 1 -image
        image_uint8 = (image * 255).astype(np.uint8)
        list_of_dicts = []
        results = cv.connectedComponentsWithStats(image_uint8, 4, cv.CV_32S)
        index = 0
        map = results[1]
        center_points = results[3]
        for result in results[2]:
            if min_size <= result[4] <= max_size and index > 0:
                x = result[0]
                y = result[1]
                width = result[2]
                height = result[3]
                mymap = map[y:y + height, x:x + width]
                mymap[mymap != index] = 0
                mymap[mymap == index] = 1
                center_point_x = int(center_points[index][0])
                center_point_y = int(center_points[index][1])
                my_dict = {'x': x, 'y': y, 'width': width, 'height': height, 'center_point_x': center_point_x,
                           'center_point_y': center_point_y, 'map': mymap}
                list_of_dicts.append(my_dict)
            index = index + 1
        return list_of_dicts

    def distance(self, x_p1, y_p1, x_p2, y_p2):
        ## we punish left and right more than because diacritic should be directly above the character it self.
        return math.sqrt((x_p2 - x_p1) ** 2 + ((y_p2 - y_p1)*0.5) ** 2)

