import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import pygame
import time
import random

# GPIO pins
attack_pin = 18
down_pin = 22
up_pin = 27
start_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(attack_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# sound
pygame.init()
start = pygame.mixer.Sound('gpio_music/start.wav')
death = pygame.mixer.Sound('gpio_music/death.wav')
attack = pygame.mixer.Sound('gpio_music/attack.wav')

# font
dogica_font_big = ImageFont.truetype("fonts/dogica/dogica.ttf", 9)
dogica_font_small = ImageFont.truetype("fonts/dogica/dogica.ttf", 8)
box_font = ImageFont.truetype("fonts/babyblocks/baby blocks.ttf", 10)
pixel_font = ImageFont.truetype("fonts/pixelmix/pixelmix.ttf", 8)


############################# Player Side ######################################
# get gpio input from the player
def get_gpio_input(display, y_inc, y_pos, up_pin, down_pin):
    if not GPIO.input(down_pin):  # if down_pin is pressed
        if y_pos + 12 >= display.height:
            y_inc = -3
        else:
            y_inc = 3

    if not GPIO.input(up_pin):  # if up_pin is pressed
        if y_pos <= 0:
            y_inc = 3
        else:
            y_inc = -3
    return y_inc


def firing_player(display, bullet_x, bullet_y, width):
    display.hline(bullet_x, bullet_y, width, 0)
    bullet_x += 20
    display.hline(bullet_x, bullet_y, width, 1)
    return bullet_x


def fire_bullet(display, player_x, player_y):
    bullet_x, bullet_y = player_x, player_y + 6
    display.hline(bullet_x, bullet_y, 10, 1)
    display.show()
    attack.play()
    return bullet_x, bullet_y


def bullet_score_check(bullet_x, bullet_y, alien_y, score, curr_level):
    fire_bullet = 1
    if curr_level == 1:
        if alien_y + 12 >= bullet_y >= alien_y and bullet_x + 10 >= 128-24:
            print("alien_y: {} {} ".format(alien_y+12, alien_y))
            print("bullet_y: ", bullet_y)
            print("bullet_x: {} {}".format(bullet_x, bullet_x+10))
            score += 1
            bullet_x, bullet_y = 0, 0
            fire_bullet = 0
        elif bullet_x + 10 >= 128-24:
            bullet_x, bullet_y = 0, 0
            fire_bullet = 0
    elif curr_level == 2 or curr_level == 3:
        if alien_y + 10 >= bullet_y >= alien_y and bullet_x + 10 >= 128-24:
            score += 1
            bullet_x, bullet_y = 0, 0
            fire_bullet = 0
        elif bullet_x + 10 >= 128-24:
            bullet_x, bullet_y = 0, 0
            fire_bullet = 0
    return bullet_x, bullet_y, score, fire_bullet

############################# Alien Side ######################################
# aline fires the bullet in a randomized size
def fire_attack(display, xpos0, ypos0, rad, col=1):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)  # (rad << 1) = length of circle
    while x >= y:
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)


def firing_alien(display, alien_x, attack_point, attack_rad):
    attack_button = 1
    fire_attack(display, alien_x, attack_point, attack_rad, 0)
    alien_x -= 8
    fire_attack(display, alien_x, attack_point, attack_rad, 1)
    return alien_x, attack_button


def firing_attack_check(attack_x, attack_y, player_y, attack_rad, lives):
    if attack_x - attack_rad <= 0 and player_y + 8 >= attack_y >= player_y:
        lives -= 1
    return lives


def firing_attack_check3(attack_x, attack_y, player_y, attack_rad, lives):
    if attack_x == 16 and player_y + 8 >= attack_y >= player_y:
        lives -= 1
    return lives


def firing_attack_check2(attack_x, attack_y, player_y, attack_rad, lives):
    if player_y + 8 >= attack_y >= player_y:
        lives -= 1
    return lives


def initialize_firing_attack(attack_range, rad):
    attack_x, attack_y = 112, random.randint(attack_range[0], attack_range[1])
    attack_rad = random.choice(rad)
    return attack_x, attack_y, attack_rad

############################# Screen Utilities ######################################
def display_start_page(display, image, draw):
    draw.text((50, 0), "Star SpaceCraft", font=dogica_font_big, fill=255)
    draw.text((85, 10), "vs", font=dogica_font_small, fill=255)
    draw.text((65, 20), "Alien", font=dogica_font_big, fill=255)
    draw.text((10, 20), "Start", font=box_font, fill=255)

    intro = Image.open('black_alien24.png').resize((24, 18), Image.ANTIALIAS).convert('1')
    display.image(image)
    display.img_display(intro, 15, 0, 0)
    time.sleep(0.5)
    display.show()

    while 1:
        if not GPIO.input(start_pin):  # start_pin is pressed
            start.play()
            display.fill(0)
            display.show()
            break
    display_load_page(display)


def display_load_page(display):
    image, draw = refresh_screen(display)
    load_percent = [i for i in range(10, 110, 10)]
    load_text = [i for i in range(20, 70, 5)]
    loading = 'Loading...'

    for i, j in enumerate(load_percent):
        display.fill(0)
        display.rect(20, 5, 100, 5, 1)
        display.rect(20, 5, j, 5, 1, fill=True)
        draw.text((load_text[i] + 20, 10), loading[i], font=dogica_font_small, fill=255)
        display.image(image)
        display.show()
        time.sleep(0.1)


def refresh_screen(display):
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)
    return image, draw


def refresh_portion_screen(width, height):
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    return image, draw


def display_time(draw, start_time, time_range, alien_y, alien_random_y):
    curr_time = int(time.time() - start_time)
    draw.text((90, 24), time_range[curr_time], font=pixel_font, fill=255)
    if curr_time % 2 == 0:
        alien_y = random.choice(alien_random_y)
    return alien_y, curr_time


def display_score(draw, score):
    draw.text((35, 24), "score: " + str(score), font=pixel_font, fill=255)


def display_lives(draw, lives):
    draw.text((35, 0), "lives: " + str(lives), font=pixel_font, fill=255)


def display_level(draw, curr_level):
    draw.text((85, 0), "Lv." + str(curr_level), font=pixel_font, fill=255)


def display_lives_color(lives):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    try:
        if lives >= 4:  # start_pin is pressed
            GPIO.output(19, True)
        elif 3 >= lives >= 2:
            GPIO.output(19, False)
            GPIO.output(13, True)
            GPIO.output(26, True)
        else:
            GPIO.output(26, True)
            GPIO.output(13, False)

    except KeyboardInterrupt:
        GPIO.cleanup()


def game_configs(curr_level):
    if curr_level == 1:
        rad = [i + 3 for i in range(5)]
        time_range = [str(i) for i in range(31)]
        alien = Image.open('black_alien24.png').resize((24, 12), Image.ANTIALIAS).convert('1')
        lives = 3
    if curr_level == 2:
        rad = [i + 3 for i in range(3)]
        time_range = [str(i) for i in range(36)]
        alien = Image.open('black_alien24.png').resize((24, 10), Image.ANTIALIAS).convert('1')
        lives = 4
    if curr_level == 3:
        rad = [i + 2 for i in range(3)]
        time_range = [str(i) for i in range(41)]
        alien = Image.open('black_alien24.png').resize((24, 10), Image.ANTIALIAS).convert('1')
        lives = 5
    return rad, time_range, alien, lives


############################## Screen Change ###########################################
def level_up_before_final(display, score, level_up, curr_level):
    if score >= level_up[curr_level-2]:  # win
        display.fill(0)
        image, draw = refresh_screen(display)

        smile = Image.open('black_smile.png').resize((32, 16), Image.ANTIALIAS).convert('1')
        display.img_display(smile, 95, 4, 0)

        draw.text((20, 22), "Quit", font=dogica_font_small, fill=255)
        draw.text((75, 22), "Next", font=dogica_font_small, fill=255)
        draw.text((10, 8), "You won!", font=dogica_font_small, fill=255)


        display.image(image)
        display.show()
        while 1:
            if not GPIO.input(up_pin):  #### QUIT ####
                display.fill(0)
                image, draw = refresh_screen(display)
                display_start_page(display, image, draw)
                play_game_display(display, curr_level=1)

            if not GPIO.input(down_pin):   #### LEVEL-UP #####
                print("go to play game display")
                play_game_display(display, curr_level)


def lose(display, score, level_up, curr_level):
    display.fill(0)
    image, draw = refresh_screen(display)
    sad = Image.open('black_sad.png').resize((32, 16), Image.ANTIALIAS).convert('1')
    display.img_display(sad, 95, 4, 0)

    draw.text((15, 22), "Quit", font=dogica_font_small, fill=255)
    draw.text((65, 22), "Replay", font=dogica_font_small, fill=255)
    draw.text((15, 8), "Score: ", font=dogica_font_small, fill=255)
    draw.text((65, 8), str(score), font=pixel_font, fill=255)
    draw.text((75, 8), "/", font=pixel_font, fill=255)
    draw.text((80, 8), str(level_up[curr_level - 1]), font=pixel_font, fill=255)
    display.image(image)
    display.show()

    while 1:
        if not GPIO.input(up_pin):   #### QUIT #### --> Back to start page
            display.fill(0)
            image, draw = refresh_screen(display)
            star = Image.open('black_star64.png').resize((32, 16), Image.ANTIALIAS).convert('1')
            display.img_display(star, 5, 6, 0)
            display.img_display(star, 85, 6, 0)

            display.fill(0)
            image, draw = refresh_screen(display)
            display_start_page(display, image, draw)
            play_game_display(display, curr_level=1)

        if not GPIO.input(down_pin):  #### BACK TO PREVIOUS LEVEL #####
            print("go to play previous level")
            play_game_display(display, curr_level)



def final_winner(display, score, level_up):
    if score >= level_up[2]:  # win
        display.fill(0)
        image, draw = refresh_screen(display)
        draw.text((15, 10), "FINAL WINNER!", font=dogica_font_big, fill=255)
        draw.text((40, 20), "Replay", font=dogica_font_small, fill=255)
        display.image(image)
        display.show()

        while 1:
            if not GPIO.input(start_pin):  # start button is pressed
                display.fill(0)
                image, draw = refresh_screen(display)
                display_start_page(display, image, draw)
                play_game_display(display, curr_level=1)



def play_game_display(display, curr_level):
    ################# Player && Alien Configs #################
    # player position
    player_x, player_y = 0, 10
    player_y_len = 12
    player_y_inc = 1

    # alien position
    alien_x, alien_y = 110, 10  # alien_x used for changing position of bullet
    alien_random_y = [i for i in range(0, 32, 3) if i + 12 < 32]

    # alien attack position
    attack_x1, attack_x2, attack_x3 = 112, 112, 112

    # display player and alien
    display.fill(0)
    rad, time_range, alien, lives = game_configs(curr_level)
    star = Image.open('black_star64.png').resize((16, 8), Image.ANTIALIAS).convert('1')
    display.img_display(star, player_x, player_y, 0)
    display.img_display(alien, alien_x, alien_y, 0)
    display.show()

    # alien attack attributes (up to 3 firing attacks -- Lv3 max)
    if curr_level == 1:
        attack_range = (alien_y, alien_y + 12)
    else:
        attack_range = (alien_y, alien_y + 10)
    attack_rad1, attack_y1 = random.choice(rad), random.randint(attack_range[0], attack_range[1])

    ################ game info ################
    # Player attack
    fire_bullet1, fire_bullet2, fire_bullet3 = 0, 0, 0

    # game display info
    curr_time = 0
    score = 0
    level_up = [5, 7, 10]
    first_alien_firing = 1
    start_time = time.time()

    while True:
        try:
            display.fill(0)
            image, draw = refresh_screen(display)

            # display lives, level, score, time
            display_level(draw, curr_level)
            display_lives(draw, lives)
            display_score(draw, score)
            alien_y, curr_time = display_time(draw, start_time, time_range, alien_y, alien_random_y)
            display.image(image)

            ###################### Randomize Alien Attack Position #############################
            if curr_level == 1:
                if attack_x1 - attack_rad1 <= 0:
                    attack_x1, attack_y1, attack_rad1 = initialize_firing_attack(attack_range, rad)

            if curr_level == 2:
                if first_alien_firing:
                    first_attack = 1
                    second_attack = 0
                if first_attack == 1 and 30 <= attack_x1 - attack_rad1 <= 35:
                    attack_x2, attack_y2, attack_rad2 = initialize_firing_attack(attack_range, rad)
                    second_attack = 1
                if first_attack == 1 and attack_x1 - attack_rad1 <= 0:
                    attack_x1, attack_y1, attack_rad1 = initialize_firing_attack(attack_range, rad)
                    first_attack = 0
                if second_attack == 1 and 30 <= attack_x2 - attack_rad2 <= 35:
                    attack_x1, attack_y1, attack_rad1 = initialize_firing_attack(attack_range, rad)
                    first_attack = 1
                if second_attack == 1 and attack_x2 - attack_rad2 <= 0:
                    attack_x2, attack_y2, attack_rad2 = initialize_firing_attack(attack_range, rad)
                    second_attack = 0
                if first_attack == 0 and second_attack == 0:
                    first_attack = 1
                    second_attack = 0

            if curr_level == 3:
                if first_alien_firing:
                    first_attack = 1
                    second_attack = 0
                    third_attack = 0

                if first_attack == 1 and attack_x1 == 64:
                    attack_x2, attack_y2, attack_rad2 = initialize_firing_attack(attack_range, rad)
                    second_attack = 1

                if first_attack == 1 and attack_x1 == 16:
                    attack_x3, attack_y3, attack_rad3 = initialize_firing_attack(attack_range, rad)
                    third_attack = 1

                if first_attack == 1 and second_attack == 1 and attack_x2 == 48:
                    attack_x1, attack_y1, attack_rad1 = initialize_firing_attack(attack_range, rad)
                    first_attack = 0

                if first_attack == 0 and second_attack == 1 and attack_x2 == 16:
                    attack_x1, attack_y1, attack_rad1 = initialize_firing_attack(attack_range, rad)
                    first_attack = 1

                if second_attack == 1 and third_attack == 1 and attack_x3 == 48:
                    attack_x2, attack_y2, attack_rad2 = initialize_firing_attack(attack_range, rad)
                    second_attack = 0

                if second_attack == 0 and third_attack == 1 and attack_x3 == 16:
                    attack_x2, attack_y2, attack_rad2 = initialize_firing_attack(attack_range, rad)
                    second_attack = 1

            ################################# Player Move ###################################
            player_y_inc = get_gpio_input(display, player_y_inc, player_y, up_pin, down_pin)

            # Alien Initiates Attack!!!
            if GPIO.input(down_pin) and GPIO.input(up_pin):
                display.img_display(star, player_x, player_y, 0)
                display.img_display(alien, alien_x, alien_y, 0)
                if curr_level == 1:
                    fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                elif curr_level == 2:
                    if first_attack == 1 and second_attack == 0:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                    if first_attack == 0 and second_attack == 1:
                        fire_attack(display, attack_x2, attack_y2, attack_rad2, 1)
                    if first_attack == 1 and second_attack == 1:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                        fire_attack(display, attack_x2, attack_y2, attack_rad2, 1)
                elif curr_level == 3:
                    if first_attack == 1 and second_attack == 0 and third_attack == 0:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                    if first_attack == 1 and second_attack == 1 and third_attack == 0:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                        fire_attack(display, attack_x2, attack_y2, attack_rad2, 1)
                    if first_attack == 1 and second_attack == 0 and third_attack == 1:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                        fire_attack(display, attack_x3, attack_y3, attack_rad3, 1)
                    if first_attack == 0 and second_attack == 1 and third_attack == 1:
                        fire_attack(display, attack_x2, attack_y2, attack_rad2, 1)
                        fire_attack(display, attack_x3, attack_y3, attack_rad3, 1)
                    if first_attack == 1 and second_attack == 1 and third_attack == 1:
                        fire_attack(display, attack_x1, attack_y1, attack_rad1, 1)
                        fire_attack(display, attack_x2, attack_y2, attack_rad2, 1)
                        fire_attack(display, attack_x3, attack_y3, attack_rad3, 1)
                display.show()
            else:
                player_y += player_y_inc
                display.img_display(star, player_x, player_y, 0)
                display.img_display(alien, alien_x, alien_y, 0)
                display.show()

            ############################ Player shooting Alien ############################
            # the number of bullet differs depending on level (lv1 - 1, lv2 - 2, lv3 - 3)
            if not GPIO.input(attack_pin):
                if curr_level == 1:
                    if fire_bullet1 == 0:
                        bullet_x1, bullet_y1 = fire_bullet(display, player_x, player_y)
                        fire_bullet1 = 1
                    elif fire_bullet1 == 1:
                        continue

                if curr_level == 2:
                    if fire_bullet1 == 0 and fire_bullet2 == 0:
                        bullet_x1, bullet_y1 = fire_bullet(display, player_x, player_y)
                        fire_bullet1 = 1
                    elif fire_bullet1 == 1 and fire_bullet2 == 0:
                        bullet_x2, bullet_y2 = fire_bullet(display, player_x, player_y)
                        fire_bullet2 = 1
                    elif fire_bullet1 == 1 and fire_bullet2 == 1:
                        continue

                if curr_level == 3:
                    if fire_bullet1 == 1 and fire_bullet2 == 1 and fire_bullet3 == 0:
                        bullet_x3, bullet_y3 = fire_bullet(display, player_x, player_y)
                        display.show()
                        fire_bullet3 = 1
                    elif fire_bullet1 == 1 and fire_bullet2 == 0 and fire_bullet3 == 0:
                        bullet_x2, bullet_y2 = fire_bullet(display, player_x, player_y)
                        fire_bullet2 = 1
                    elif fire_bullet1 == 0 and fire_bullet2 == 0 and fire_bullet3 == 0:
                        bullet_x1, bullet_y1 = fire_bullet(display, player_x, player_y)
                        fire_bullet1 = 1

            if fire_bullet1 == 1:
                bullet_x1 = firing_player(display, bullet_x1, bullet_y1, 10)
                bullet_x1, bullet_y1, score, fire_bullet1 = bullet_score_check(bullet_x1, bullet_y1, alien_y,
                                                                                    score, curr_level)
            if fire_bullet2 == 1:
                bullet_x2 = firing_player(display, bullet_x2, bullet_y2, 10)
                bullet_x2, bullet_y2, score, fire_bullet2 = bullet_score_check(bullet_x2, bullet_y2, alien_y,
                                                                                    score, curr_level)
            if fire_bullet3 == 1:
                bullet_x3 = firing_player(display, bullet_x3, bullet_y3, 10)
                bullet_x3, bullet_y3, score, fire_bullet3 = bullet_score_check(bullet_x3, bullet_y3, alien_y,
                                                                                    score, curr_level)

            ############################### Alien Attacking Player ####################################
            if curr_level == 1:
                attack_x1, first_attack = firing_alien(display, attack_x1, attack_y1, attack_rad1)
                lives = firing_attack_check(attack_x1, attack_y1, player_y, attack_rad1, lives)
            elif curr_level == 2:
                if first_attack == 1:
                    attack_x1, first_attack = firing_alien(display, attack_x1, attack_y1, attack_rad1)
                    lives = firing_attack_check(attack_x1, attack_y1, player_y, attack_rad1, lives)
                if second_attack == 1:
                    attack_x2, second_attack = firing_alien(display, attack_x2, attack_y2, attack_rad2)
                    lives = firing_attack_check(attack_x2, attack_y2, player_y, attack_rad2, lives)
            elif curr_level == 3:
                if first_attack == 1:
                    attack_x1, first_attack = firing_alien(display, attack_x1, attack_y1, attack_rad1)
                    print("attack_x1: ", attack_x1)
                    lives = firing_attack_check3(attack_x1, attack_y1, player_y, attack_rad1, lives)
                if second_attack == 1:
                    attack_x2, second_attack = firing_alien(display, attack_x2, attack_y2, attack_rad2)
                    print("attack_x2: ", attack_x2)
                    lives = firing_attack_check3(attack_x2, attack_y2, player_y, attack_rad2, lives)
                if third_attack == 1:
                    attack_x3, third_attack = firing_alien(display, attack_x3, attack_y3, attack_rad3)
                    print("attack_x3: ", attack_x3)
                    lives = firing_attack_check3(attack_x3, attack_y3, player_y, attack_rad3, lives)

            first_alien_firing = 0

            ############################### State of Player by LED Light ##############################
            display_lives_color(lives)
            display.show()

            ################################ Exceptions Handling #######################################
            if curr_time == int(time_range[-1]):
                display.clear_buffer()
                print("Time Over!!!")
                death.play()
                lose(display, score, level_up, curr_level)
            if lives == 0:
                por_image, por_draw = refresh_portion_screen(10, 3)
                display_lives(por_draw, lives)
                display.image(por_image)
                display.show()
                display.clear_buffer()
                print("You are Dead!!!")
                death.play()
                lose(display, score, level_up, curr_level)
            ################################ Congratulations Level-Up #######################################
            if curr_level == 1 and score >= level_up[0]:
                curr_level += 1
                print("level up to 2")
                image, draw = refresh_screen(display)
                display_score(draw, score)
                display.image(image)
                display.show()
                level_up_before_final(display, score, level_up, curr_level)
            elif curr_level == 2 and score >= level_up[1]:
                curr_level += 1
                image, draw = refresh_screen(display)
                display_score(draw, score)
                display.image(image)
                display.show()
                print("level up to 3")
                level_up_before_final(display, score, level_up, curr_level)
            elif curr_level == 3 and score >= level_up[2]:
                print("you are the real starcraft!")
                final_winner(display, score, level_up)

        except KeyboardInterrupt:
            display.clear_buffer()
            display.clear_display(0, 0, 128, 32)
            print("program ended!!!")
            break

