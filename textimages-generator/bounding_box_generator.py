class BboxGenerator:
    def draw_bounding_box(self, font, image, draw, text_until_current_char, current_character):
        base_character = self.retrieve_base_character(current_character)
        current_character_coordinates = (5 + font.getlength(text_until_current_char) , 5)
        bbox_base_character = draw.textbbox(current_character_coordinates, base_character, font = font)
        bbox_accent = draw.textbbox(current_character_coordinates, current_character, font=font)
        bbox_only_accent = [bbox_accent[0], 
                                bbox_accent[1], 
                                bbox_accent[2], 
                                bbox_accent[3] - (bbox_base_character[3] - bbox_base_character[1])]
        

        bbox_accent_adjusted = [bbox_only_accent[0] + self.adjust_left(bbox_only_accent, image), 
                                bbox_only_accent[1],
                                bbox_only_accent[2] - self.adjust_right(bbox_only_accent, image), 
                                bbox_only_accent[3] - self.adjust_bottom(bbox_only_accent, image)]

        draw.rectangle(bbox_accent_adjusted, outline="blue")

    def adjust_left(self, bbox_accent, image):
        current_bbox_height = bbox_accent[3] - bbox_accent[1] 
        current_bbox_width = bbox_accent[0] - bbox_accent[2] 

        for x_offset in range(int(current_bbox_width)):
            for y_offset in range(current_bbox_height):
                pixel = image.getpixel((bbox_accent[0] + x_offset, bbox_accent[1] + y_offset))
                if pixel == 0:
                    return x_offset - 1 
        return 0


    def adjust_right(self, bbox_accent, image):
        current_bbox_height = bbox_accent[3] - bbox_accent[1] 
        current_bbox_width = bbox_accent[0] - bbox_accent[2] 

        for x_offset in range(int(current_bbox_width)):
            for y_offset in range(current_bbox_height):
                pixel = image.getpixel((bbox_accent[2] - x_offset, bbox_accent[1] + y_offset))
                if pixel == 0:
                    return x_offset - 1       
        return 0
                
    def adjust_bottom(self, bbox_accent, image):
        current_bbox_height = bbox_accent[3] - bbox_accent[1] 
        current_bbox_width = bbox_accent[2] - bbox_accent[0]

        for y_offset in range(int(current_bbox_height)):
            for x_offset in range(int(current_bbox_width)):
                pixel = image.getpixel((bbox_accent[0] + x_offset, (bbox_accent[3] - 1) - y_offset))
                if pixel == 0:
                    return y_offset
        return 0
                
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