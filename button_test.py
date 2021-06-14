import RPi.GPIO as GPIO

start = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while 1:
    if not GPIO.input(start):
        print("test end!")
        break
