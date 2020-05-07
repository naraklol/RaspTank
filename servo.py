import Adafruit_PCA9685
import time

# initialize the servo-controller and set the pwm frequency
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Servo parent class with servo parameters
class Servo():

    # Initialize a new servomotor
    def __init__(self, init, max, min, channel):
        self.init = init
        self.max = max
        self.min = min
        self.pos = init
        self.channel = channel
        self.update_position()

    # Update the position of the servo by sending a PWM signal
    def update_position(self):
        pwm.set_pwm(self.channel, 0, self.pos)

    # Change the position of the servo to a set position
    def set_position(self, value):
        self.pos = value
        if self.pos > self.max:
            self.pos = self.max
        if self.pos < self.min:
            self.pos = self.min
        self.update_position()

    # Increment the current position by a value
    # Overrides the '+' operator for the class
    def __add__(self, value):
        self.pos += value
        if self.pos > self.max:
            self.pos = self.max
        self.update_position()
        return self
    
    # Decrement the current position by a value
    # Overrides the '-' operator for the class
    def __sub__(self, value):
        self.pos -= value
        if self.pos < self.min:
            self.pos = self.min
        self.update_position()
        return self

# CameraServo child class
class CameraServo(Servo):
    def up(self, value):
        self -= value
    def down(self, value):
        self += value

# ClawServo child class
class ClawServo(Servo):
    def loose(self):
        self.set_position(self.min)
        self.update_position()
    def grab(self):
        self.set_position(self.max)
        self.update_position()

# ClawAngleServo child class
class ClawAngleServo(Servo):
    def clockwise(self, value):
        self.pos -= value
        self.update_position()
    def counterclockwise(self, value):
        self.pos += value
        self.update_position()
    
# ArmServo child class
class ArmServo(Servo):
    def up(self, value):
        self.pos -= value
        self.update_position()
    def down(self, value):
        self.pos += value
        self.update_position()

# BaseServo child class
class BaseServo(Servo):
    def forward(self, value):
        self.pos -= value
        self.update_position()
    def backward(self, value):
        self.pos += value
        self.update_position()

# initialize all the servomotors with their respective classes and initial values
camera = CameraServo(init=300, max=500, min=100, channel=11)
claw = ClawServo(init=350, max=350, min=100, channel=15)
claw_angle = ClawAngleServo(init=350, max=350, min=100, channel=14) # servo doesnt respond
arm = ArmServo(init=100, max=500, min=100, channel=13)
base = BaseServo(init=300, max=500, min=100, channel=12)

# allow the servomotors to set their initial positions
time.sleep(1)

while True:
    claw.loose()
    time.sleep(1)
    claw.grab()
    time.sleep(1)