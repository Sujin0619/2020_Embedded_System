import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

try:
    while 1:
        GPIO.output(26, True)
        time.sleep(0.5)
        GPIO.output(26, False)
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

