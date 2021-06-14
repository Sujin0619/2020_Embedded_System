import pygame
from gpiozero import Button

# init sound files
pygame.init()
btn = Button(17)


start = pygame.mixer.Sound('/home/pi/spacecraft/gpio_music/start.wav')
death = pygame.mixer.Sound('/home/pi/spacecraft/gpio_music/death.wav')
attack = pygame.mixer.Sound('/home/pi/spacecraft/gpio_music/attack.wav')


def hello():
    print("hello")
    start.play()

while True:
	btn.when_pressed = start.play
