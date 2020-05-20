import RPi.GPIO as GPIO
import time
from move import Motor
from servo_0520 import Servo

'''
Black tape problem: It reflects the lights, so the black tape is considered to bright.
In contrast, regular floor is considered to be dark (when there's no sun light)
That's why straight, left, right, and backward are flipped in this code
'''


# GPIO 19 right: Pin35
# GPIO 16 middle: Pin36
# GPIO 20 left: Pin38

pin_right = 19
pin_middle = 16
pin_left = 20

dir_forward   = 0
dir_backward  = 1

turn_no = 0
turn_left = 1
turn_right = 2

reset = 0
reached_to_obj = 1
picked_obj = 2
head_to_base = 3
reached_to_base = 4
tank_pos_init = 5


class LineTrack():

    def __init__(self, direction, turn):
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_right,GPIO.IN)
        GPIO.setup(pin_middle,GPIO.IN)
        GPIO.setup(pin_left,GPIO.IN)
        
        self.direction = direction
        self.turn = turn

        self.status = reset

    # This detects only 1 and 0
    # Dark 0, bright 1
    # motor from move.py class Motor
    def Run(self, motor):

        right = GPIO.input(pin_right)
        middle = GPIO.input(pin_middle)
        left = GPIO.input(pin_left)
        print('R%d   M%d   L%d'%(right,middle,left))
        
        if(left == 1 and middle == 0 and right == 0): # turn right
            if(self.direction == dir_forward):
                motor.Move('backward', 'left')
            else:
                motor.Move('forward', 'left')
            self.turn = turn_right
            print('turn right')
        elif(left == 0 and middle == 0 and right == 1): # turn left
            if(self.direction == dir_forward):
                motor.Move('backward', 'right')
            else:
                motor.Move('forward', 'right')
            self.turn = turn_left
            print('turn left')
        elif(left == 0 and middle == 1 and right == 1):
            motor.Move('backward', 'straight')
            self.direction = dir_forward
            self.turn = turn_no
            print('Forward')
        elif(right == 0 and middle == 1 and left == 1):
            motor.Move('backward', 'straight')
            self.direction = dir_forward
            self.turn = turn_no
            print('Forward')
        # black(Dark)
        elif(left == 1 and middle == 1 and right == 1):
                motor.Move('backward', 'straight')
                self.direction = dir_forward
                self.turn = turn_no
                print('Forward')
        elif(left == 0 and middle == 1 and right == 0):
                motor.Move('backward', 'straight')
                self.direction = dir_forward
                self.turn = turn_no
                print('Forward')
        else: # move forward
            self.__end__(motor)
            if(self.turn == turn_left):
                for i in range (0,10000):
                    motor.Move('backward', 'right')
                    print('turning left')
            elif(self.turn == turn_right):
                for i in range (0,10000):
                    motor.Move('backward', 'left')
                    print('turning right')

            if(self.turn == turn_no):
                if(self.status == reset):
                    self.status = reached_to_obj
                    print('reached to the object')
                elif(self.status == picked_obj):
                    self.status = head_to_base
                    print('head to the base')
                    #rotate 180 and come back to the starting point
                    for i in range (0,70000):
                        motor.Move('backward', 'left')
                        print('turning right 180 degree')
                elif(self.status == head_to_base):
                    self.status = reached_to_base
                    print('reached to the base')
                elif(self.status == tank_pos_init):
                    self.status = reset
                    print('reset')
                    #rotate 180 and come back to the starting point
                    if(self.turn == turn_left):
                        for i in range (0,70000):
                            motor.Move('backward', 'left')
                            print('turning right 180 degree')
                    elif(self.turn == turn_right):
                        for i in range (0,70000):
                            motor.Move('backward', 'right')
                            print('turning left 180 degree')

                self.__end__(motor)
        

    def GetStatus(self):
        return self.status

    def SetStatus(self, status):
        self.status = status
            
            
    def __end__(self, motor):
        motor.__end__()
        print('end')
        
        
try:
    track = LineTrack(dir_forward, turn_no)
    motor = Motor(50) #move.setup()
    servo = Servo()
    while 1:
        track.Run(motor)
        if(track.GetStatus() == reached_to_obj):
            servo.pickup()
            track.SetStatus(picked_obj)
            print('object pick up')
        elif(track.GetStatus() == reached_to_base):
            servo.drop()
            track.SetStatus(tank_pos_init)
            print('object drop')
        

except KeyboardInterrupt:
    track.__end__(motor)
