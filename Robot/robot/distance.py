import RPi.GPIO as GPIO
import robot.pins as pins
from threading import Thread
import time

_measuring = False
_d = 0
_thread = None
_callback = None

HALF_CIRCUMFERENCE = 10.21

GPIO.setup(pins.HALL_EFFECT, GPIO.IN)

def _measure():
    global _measuring
    global _callback
    last = []
    for i in range(15):
        last.append(1)
    while _measuring:
        now = GPIO.input(pins.HALL_EFFECT)

        if now == 0 and sum(last) == 15:
            _callback()

        for i in range(14, 0):
            last[i] = last[i - 1]
        last[0] = now
        time.sleep(0.01)

def start_measuring(callback):
    global _measuring
    global _d
    global _callback
    global _thread
    if not _measuring:
        _measuring = True
        _d = 0
        _callback = callback
        _thread = Thread(target=_measure)
        _thread.start()

def stop_measuring():
    global _measuring
    global _thread
    _measuring = False
    _thread.join()

def get_distance():
    return _d