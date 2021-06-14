from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
import pygame
from gpiozero import Button
import time
import random
import game_func as func

i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display
display.fill(0)
display.show()

image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Load fonts
dogica_font_big = ImageFont.truetype("fonts/dogica/dogica.ttf", 9)
dogica_font_small = ImageFont.truetype("fonts/dogica/dogica.ttf", 8)
box_font = ImageFont.truetype("fonts/babyblocks/baby blocks.ttf", 10)
pixel_font = ImageFont.truetype("fonts/pixelmix/pixelmix.ttf", 8)

time_range = [str(i) for i in range(10)]


for i in range(3):
   draw.text((90, 24), time_range[i], font=pixel_font, fill=255)
   display.image(image)
   display.show()
   time.sleep(1)
   display.clear_display(90,24,30,10)
   display.show()
   

#intro = Image.open('black_alien24.png').resize((24,18),Image.ANTIALIAS).convert('1')

