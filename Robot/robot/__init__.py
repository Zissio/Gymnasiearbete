from subprocess import call
import RPi.GPIO as GPIO
import robot.pins as pins
import time
import math

_battery_callback = None
_battery_pauses = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pins.BATTERY, GPIO.IN)

def on_battery_low(callback):
    global _battery_callback
    _battery_callback = callback
    GPIO.remove_event_detect(pins.BATTERY)
    GPIO.add_event_detect(pins.BATTERY, GPIO.FALLING, callback=lambda a: callback(), bouncetime=300)

def pause_battery_detection():
    global _battery_pauses
    GPIO.remove_event_detect(pins.BATTERY)
    _battery_pauses += 1

def resume_battery_detection():
    global _battery_pauses
    _battery_pauses -= 1
    if not _battery_callback is None and _battery_pauses == 0:
        on_battery_low(_battery_callback)

def halt():
    call(["halt"])


import robot.compass as compass
import robot.motors as motors

def turn_to(heading, error=1):
    while abs(math.degrees(math.atan2(math.sin(math.radians(compass.getHeading() - heading)), math.cos(math.radians(compass.getHeading() - heading))))) > error:
        while abs(math.degrees(math.atan2(math.sin(math.radians(compass.getHeading() - heading)), math.cos(math.radians(compass.getHeading() - heading))))) > error:
            if abs(math.degrees(math.atan2(math.sin(math.radians(compass.getHeading() - heading)), math.cos(math.radians(compass.getHeading() - heading))))) < 0:
                motors.left(50)
            else:
                motors.right(50)
        motors.stop()
        time.sleep(1)