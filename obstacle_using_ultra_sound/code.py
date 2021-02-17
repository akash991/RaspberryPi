import time
import RPi.GPIO as GPIO
from RPi_GPIO_i2c_LCD import lcd

"""
Setting pin configuration
1. Select GPIO17 as input
2. Select GPIO27 as output
3. Set I2C address for the 16x2 i2c
4. Create instance of lcd
5. Clear the 16x2 display
"""
TRIG = 17
ECHO = 27
i2c_address = 0x27
lcdDisplay = lcd.HD44780(i2c_address)
lcdDisplay.clear()

"""
1. Set mode for General I/O
2. Set TRIG as OUT
3. Set ECHO as IN
"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

while True:
    """
    1. Set TRIG to 0
    2. Set TRIG to 1 for 10us
    3. Set TRIG to 0

    ECHO starts as LOW and becomes HIGH
    after the US is reflected by an obstacle.

    Total time taken = duration for which ECHO remains LOW
    """
    GPIO.output(TRIG, False)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) ==  0:
        pulse_start = time.time()

    while GPIO.input(ECHO) ==  1:
        pulse_stop = time.time()

    pulse_duration = pulse_stop - pulse_start

    """
    speed = distance / time
    34300 cm/s = (2 * distance in cm) / time
    distance (cm) = 34300 * time / 2
    distance (cm) = 17150 * time

    Note: here, we do 2 * distance because first the waves are transmitted.
    They travel some distance, hit an obstacle gets reflected and again travel the same distance.
    """
    distance = 17150 * pulse_duration

    """
    Print how far the obstacle is from the source.
    """
    lcdDisplay.set("{0:.3f} cm".format(distance), 1)

GPIO.cleanup()