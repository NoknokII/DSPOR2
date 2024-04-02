from PIL import Image, ImageDraw, ImageFont

width, height = 400, 200
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

font_size = 150
font = ImageFont.truetype('textimages-generator/fonts/LoveDays-2v7Oe.ttf', font_size)

text = "eéèê"

# Draw the text
imageDraw = draw.text((5, 5), text, fill="black", font=font)


bbox_e = draw.textbbox((5, 5), 'e', font=font)
draw.rectangle(bbox_e, outline="red")

def draw_bounding_box_accent(character_with_diacritic, character_index):
    bbox_e_accent = draw.textbbox((5 + font.getlength(text[:character_index]) , 5), character_with_diacritic, font=font)
    bbox_only_accent = [bbox_e_accent[0], 
                              bbox_e_accent[1], 
                              bbox_e_accent[2], 
                              bbox_e_accent[3] - (bbox_e[3] - bbox_e[1])]
    

    bbox_e_accent_adjusted = [bbox_only_accent[0] + adjust_left(bbox_only_accent), 
                              bbox_only_accent[1],
                              bbox_only_accent[2] - adjust_right(bbox_only_accent), 
                              bbox_only_accent[3] - adjust_bottom(bbox_only_accent)]

    draw.rectangle(bbox_e_accent_adjusted, outline="blue")

def adjust_left(bbox_accent):
    current_bbox_height = bbox_accent[3] - bbox_accent[1] 

    for x_offset in range(int(width - bbox_accent[0])):
        for y_offset in range(current_bbox_height):
            pixel = image.getpixel((bbox_accent[0] + x_offset, bbox_accent[1] + y_offset))
            if pixel == (0, 0, 0):
                return x_offset - 1         

def adjust_right(bbox_accent):
    current_bbox_height = bbox_accent[3] - bbox_accent[1] 

    for x_offset in range(int(bbox_accent[2])):
        for y_offset in range(current_bbox_height):
            pixel = image.getpixel((bbox_accent[2] - x_offset, bbox_accent[1] + y_offset))
            if pixel == (0, 0, 0):
                return x_offset - 1       
            
def adjust_bottom(bbox_accent):
    current_bbox_width = bbox_accent[2] - bbox_accent[0] 

    for y_offset in range(int(current_bbox_width)):
        for x_offset in range(int(width - bbox_accent[0])):
            pixel = image.getpixel((bbox_accent[0] + x_offset, bbox_accent[3] - y_offset))
            if pixel == (0, 0, 0):
                return y_offset - 1  
    
draw_bounding_box_accent('é', 1)
draw_bounding_box_accent('è', 2)
draw_bounding_box_accent('ê', 3)

# Show the image
image.save("./boundingboxes.png")