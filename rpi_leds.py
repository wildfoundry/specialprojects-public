import RPi.GPIO as GPIO
import time

LED_COLOR = ("green",
             "red")

LED_MAP = {LED_COLOR[0]: 16,
           LED_COLOR[1]: 18}


def setup():
    GPIO.setmode(GPIO.BOARD)
    for i in LED_COLOR:
        GPIO.setup(LED_MAP[i], GPIO.OUT)

def control(led, state):
    GPIO.output(led, state)

def cleanup():
    GPIO.cleanup()


if __name__ == "__main__":

    setup()

    for i in LED_COLOR:
        GPIO.output(LED_MAP[i], 1)

    time.sleep(2)

    cleanup()
