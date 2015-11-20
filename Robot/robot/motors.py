import RPi.GPIO as GPIO
import robot.pins as pins

class Motor:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2

        GPIO.setup(pin1, GPIO.OUT, initial=False)
        GPIO.setup(pin2, GPIO.OUT, initial=False)

    def forward(self):
        GPIO.output(self.pin1, True)
        GPIO.output(self.pin2, False)

    def backward(self):
        GPIO.output(self.pin2, True)
        GPIO.output(self.pin1, False)

    def stop(self):
        GPIO.output(self.pin1, False)
        GPIO.output(self.pin2, False)

LEFT = Motor(pins.MOTOR_LEFT_1, pins.MOTOR_LEFT_2)
RIGHT = Motor(pins.MOTOR_RIGHT_1, pins.MOTOR_RIGHT_2)

def stop():
    LEFT.stop()
    RIGHT.stop()