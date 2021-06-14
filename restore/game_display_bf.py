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
# func.display_start_page(display, image, draw)

# display loading page
# func.display_load_page(display)


# player position
x_pos, y_pos = 0, 10
y_len = 12
y_inc = 1

# alien position
alien_x, alien_y = 110, 10  # alien_x used for changing position of bullet
alien_random_y = [i for i in range(0, 32, 3) if i + 12 < 32]

# alien attack position
attack_x1, attack_x2, attack_x3 = 110, 110, 110
attack_range = (alien_y, alien_y + 12)

# alien attack attributes
rad = [i + 1 for i in range(5)]
attack_point = random.randint(attack_range[0], attack_range[1])
attack_rad = random.choice(rad)

# display player and alien
display.fill(0)
star = Image.open('black_star64.png').resize((20, 8), Image.ANTIALIAS).convert('1')
alien = Image.open('black_alien24.png').resize((24, 12), Image.ANTIALIAS).convert('1')
display.img_display(star, x_pos, y_pos, 0)
display.img_display(alien, attack_x1, alien_y, 0)
display.show()

# state display
time_range = [str(i) for i in range(91)]

# game info
start_time = time.time()
second_attack, third_attack, fire_bullet = 0, 0, 0
fire_bullet2 = 0
fire_bullet3 = 0

curr_level = 1
curr_time = 0
level_up = [8, 12, 15]
score = 0
lives = 5

while True:
    try:
        display.fill(0)
        image, draw = func.refresh_screen(display)

        # display lives, level, score, time
        func.display_level(draw, curr_level)
        func.display_lives(draw, lives)
        func.display_score(draw, score)
        alien_y, curr_time = func.display_time(draw, start_time, time_range, alien_y, alien_random_y)
        display.image(image)

        # depending on the level
        if curr_level == 1:
            if attack_x1 - attack_rad <= 0:
                attack_x1 = 110
                attack_point = random.randint(attack_range[0],
                                              attack_range[1])  # y-axis => fixed until bullet hits the wall
                attack_rad = random.choice(rad)

        y_inc = func.get_gpio_input(display, y_inc, y_pos, up_pin, down_pin)

        # Player move upward or downward
        if GPIO.input(down_pin) and GPIO.input(up_pin):
            display.img_display(star, x_pos, y_pos, 0)
            display.img_display(alien, alien_x, alien_y, 0)
            func.fire_attack(display, attack_x1, attack_point, attack_rad, 1)
            # if second_attack == 1:
            #     func.fire_attack(display, attack_x2, attack_point2, attack_rad2, 1)
            display.show()
        else:
            y_pos += y_inc
            display.img_display(star, x_pos, y_pos, 0)
            display.img_display(alien, alien_x, alien_y, 0)
            display.show()

        # Player attacks alien
        if not GPIO.input(attack_pin):
            if fire_bullet == 1 and fire_bullet2 == 1 and fire_bullet3 == 0:
                bullet_x3 = x_pos
                bullet_y3 = y_pos + 6
                display.hline(bullet_x3, bullet_y3, 10, 1)
                display.show()
                fire_bullet3 = 1
            elif fire_bullet == 1 and fire_bullet2 == 0 and fire_bullet3 == 0:
                bullet_x2 = x_pos
                bullet_y2 = y_pos + 6
                display.hline(bullet_x2, bullet_y2, 10, 1)
                display.show()
                fire_bullet2 = 1
            elif fire_bullet == 0 and fire_bullet2 == 0 and fire_bullet3 == 0:
                bullet_x = x_pos
                bullet_y = y_pos + 6
                display.hline(bullet_x, bullet_y, 10, 1)
                display.show()
                fire_bullet = 1

        attack_x1 = func.firing_alien(display, attack_x1, attack_point, attack_rad)
        # if second_attack == 1:
        #     attack_x2 = func.firing_alien(display, attack_x2, attack_point2, attack_rad2)

        if fire_bullet == 1:
            bullet_x = func.firing_player(display, bullet_x, bullet_y, 10)
            if alien_y + 12 >= bullet_y >= alien_y and bullet_x + 10 >= 128:
                score += 1
                bullet_x, bullet_y = 0, 0
                fire_bullet = 0

        if fire_bullet2 == 1:
            bullet_x2 = func.firing_player(display, bullet_x2, bullet_y2, 10)
            if alien_y + 12 >= bullet_y2 >= alien_y and bullet_x2 + 10 >= 128:
                score += 1
                bullet_x2, bullet_y2 = 0, 0
                fire_bullet2 = 0

        if fire_bullet3 == 1:
            bullet_x3 = func.firing_player(display, bullet_x3, bullet_y3, 10)
            if alien_y + 12 >= bullet_y3 >= alien_y and bullet_x3 + 10 >= 128:
                score += 1
                bullet_x3, bullet_y3 = 0, 0
                fire_bullet3 = 0

        if attack_x1 - attack_rad <= 0 and y_pos + 8 >= attack_point >= y_pos:
            lives -= 1

        func.display_lives_color(lives)

        # if lives == 0 or curr_time == 90:
        #     if curr_level == 1:
        #         if score >= level_up[0]:

        display.show()
    except KeyboardInterrupt:
        display.clear_display(0, 0, 128, 32)
        print("program ended!")
        break

