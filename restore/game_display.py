from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
import time
import random
import game_func as func

# button_config
down_pin = 18
up_pin = 23
start_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display
display.fill(0)
display.show()

# game start screen
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)


# Load fonts
dogica_font_big = ImageFont.truetype("fonts/dogica/dogica.ttf", 9)
dogica_font_small = ImageFont.truetype("fonts/dogica/dogica.ttf", 8)
box_font = ImageFont.truetype("fonts/babyblocks/baby blocks.ttf", 10)
barcode_font = ImageFont.truetype("fonts/paskowy/Paskowy.ttf", 10)

# text
draw.text((50, 0), "Star SpaceCraft", font=dogica_font_big, fill=255)
draw.text((85, 10), "vs", font=dogica_font_small, fill=255)
draw.text((65, 20), "Alien", font=dogica_font_big, fill=255)
draw.text((10, 20), "Start", font=box_font, fill=255)

# img
intro = Image.open('alien.png').resize((16, 16), Image.ANTIALIAS).convert('1')

display.image(image)
display.img_display(intro, 15, 0, 0)
display.show()

# loading check
load_percent = [i for i in range(10, 110, 10)]
load_text = [i for i in range(20, 70, 5)]
loading = 'Loading...'

while 1:
    if GPIO.input(start_pin):  # start_pin is pressed
        display.fill(0)
        display.show()
        break

# refresh image
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

for i, j in enumerate(load_percent):
    display.fill(0)
    display.rect(20, 5, 100, 5, 1)
    display.rect(20, 5, j, 5, 1, fill=True)
    draw.text((load_text[i]+20, 10), loading[i], font=dogica_font_small, fill=255)
    display.image(image)
    display.show()
    time.sleep(0.1)


# player position
x_pos = 0
y_pos = 10
y_len = 16
y_inc = 1

# alien position
alien_x = 110
alien_fixed_x = 110
alien_y = 10
alien_random_y = [i for i in range(0, 32, 3) if i+16 < 32]
#alien_random_y = [i for i in range(0, 32, 4) if i+16 < 32]
attack_range = (alien_y, alien_y + 16)

# circle radius
rad = [i+1 for i in range(6)]

# display player and alien
display.fill(0)
star = Image.open('star.png').resize((16, 16), Image.ANTIALIAS).convert('1')
alien = Image.open('aircraft.png').resize((16, 16), Image.ANTIALIAS).convert('1')
display.img_display(star, x_pos, y_pos, 0)
display.img_display(alien, alien_x, alien_y, 0)
display.show()

while True:
    display.fill(0)
    # randomly choose alien y_pos, attack_point, attack_rad
    alien_y = random.choice(alien_random_y)
    attack_point = random.randint(attack_range[0], attack_range[1])
    attack_rad = random.choice(rad)
    if alien_x < 0: alien_x = 110

    y_inc = func.get_gpio_input(display, y_inc, y_pos, up_pin, down_pin)

    if not GPIO.input(down_pin) and not GPIO.input(up_pin):
        display.img_display(star, x_pos, y_pos, 0)
        display.img_display(alien, alien_fixed_x, alien_y, 0)
        func.fire_attack(display, alien_x, attack_point, attack_rad, 1)
        display.show()
    else:
        y_pos += y_inc
        display.img_display(star, x_pos, y_pos, 0)
        display.img_display(alien, alien_fixed_x, alien_y, 0)
        func.fire_attack(display, alien_x, attack_point, attack_rad, 1)
        display.show()

    alien_x = func.firing_alien(display, alien_x, attack_point, attack_rad)




















