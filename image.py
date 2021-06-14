
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import game_func as func

dogica_font_big = ImageFont.truetype("fonts/dogica/dogica.ttf", 9)

i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

image, draw = func.refresh_screen(display)

display.fill(0)
#smile = Image.open('black_smile.png').resize((32, 16), Image.ANTIALIAS).convert('1')
#sad = Image.open('black_sad.png').resize((32, 16), Image.ANTIALIAS).convert('1')
star = Image.open('black_star64.png').resize((32, 16), Image.ANTIALIAS).convert('1')

#display.img_display(smile, 90, 6, 0)
#display.img_display(sad, 95, 6, 0)
display.img_display(star, 85, 6, 0)
display.img_display(star, 5, 6, 0)

draw.text((35, 10), "Finish", font=dogica_font_big, fill=255)
#draw.text((65, 22), "Replay", font=dogica_font_big, fill=255)
#draw.text((10, 8), "Score: ", font=dogica_font_big, fill=255)
#draw.text((70, 8), "17", font=dogica_font_big, fill=255)

display.image(image)

display.show()
