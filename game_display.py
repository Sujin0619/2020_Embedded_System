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

# button_config
attack_pin = 18
down_pin = 22
up_pin = 27
start_pin = 17

# GIP.PUD_UP mode -> default = 1 (button is released), 0 (button is pressed)
GPIO.setmode(GPIO.BCM)
GPIO.setup(attack_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# init sound files
pygame.init()
start = pygame.mixer.Sound('gpio_music/start.wav')
death = pygame.mixer.Sound('gpio_music/death.wav')
attack = pygame.mixer.Sound('gpio_music/attack.wav')

i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display
display.fill(0)
display.show()

# game start screen
image, draw = func.refresh_screen(display)

# display start page
func.display_start_page(display, image, draw)

# display loading page
# func.display_load_page(display)

curr_level = 1
func.play_game_display(display, curr_level)
