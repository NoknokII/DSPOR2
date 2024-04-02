from PIL import Image, ImageDraw, ImageFont
from bounding_box_generator import BboxGenerator

width, height = 400, 200
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

font_size = 150
font = ImageFont.truetype('textimages-generator/fonts/LoveDays-2v7Oe.ttf', font_size)

text = "abîma"

# Draw the text
imageDraw = draw.text((5, 5), text, fill="black", font=font)

bbox_generator =  BboxGenerator()

bbox_generator.draw_bounding_box(font, image, draw, 'abî', 'î')