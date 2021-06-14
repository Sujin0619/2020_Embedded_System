import RPi.GPIO as GPIO
import pygame

pygame.init()
attack = pygame.mixer.Sound('gpio_music/attack.wav')

def get_gpio_input(display, y_inc, y_pos, up_pin, down_pin):
    if GPIO.input(down_pin):
        if y_pos + 12 >= display.height:
            y_inc = -3
        else:
            y_inc = 3

    if GPIO.input(up_pin):
        if y_pos <= 0:
            y_inc = 3
        else:
            y_inc = -3
    return y_inc


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
    attack.play()


def firing_alien(display, alien_x, attack_point, attack_rad):
    fire_attack(display, alien_x, attack_point, attack_rad, 0)
    alien_x -= 7
    fire_attack(display, alien_x, attack_point, attack_rad, 1)
    display.show()
    return alien_x
