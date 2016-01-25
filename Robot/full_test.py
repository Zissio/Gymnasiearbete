from robot import compass
from robot import motors
from robot import distance
import robot
import math

n = 0

def count():
    global n
    n += 1

def avsluta():
    print("Batteriet är slut!")
    robot.clean()
    robot.halt()

try:
    compass.calibrate(5)
    robot.turn_to(math.pi/2, math.radians(4))
    input("Enter")
    distance.start_measuring(count)
    motors.forward(math.pi/2)
    input("Tryck på enter")
    motors.stop()
    distance.stop_measuring()
    print("Antal halva varv: {}".format(n))
    robot.turn_to(3*math.pi/2, math.radians(4))
    motors.forward(3*math.pi/2)
    input("Tryck på enter för att stanna")
finally:
    motors.stop()
    robot.clean()