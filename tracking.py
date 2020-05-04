import RPi.GPIO as GPIO
import time
from move import Motor

'''
Black tape problem: It reflects the lights, so the black tape is considered to bright.
In contrast, regular floor is considered to be dark (when there's no sun light)
That's why straight, left, right, and backward are flipped in this code
'''

'''
To-do List
 1) Check the tracking with the upgraded version of move.py
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

class LineTrack():

    def __init__(self, direction, turn):
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_right,GPIO.IN)
        GPIO.setup(pin_middle,GPIO.IN)
        GPIO.setup(pin_left,GPIO.IN)
        
        self.direction = direction
        self.turn = turn
        self.previous_turn = turn_no
        self.count = 0

    # This detects only 1 and 0
    # Dark 0, bright 1
    # motor from move.py class Motor
    def Run(self, motor):

        right = GPIO.input(pin_right)
        middle = GPIO.input(pin_middle)
        left = GPIO.input(pin_left)
        print('R%d   M%d   L%d'%(right,middle,left))
        
        
        if(left == 1 and right == 0): # turn right
            if(self.direction == dir_forward):
                motor.Move('backward', 'left')
            else:
                motor.Move('forward', 'left')
            self.turn = turn_left
            #print('turn left') # originally right
            self.count = 0
        elif(left == 0 and right == 1): # turn left
            if(self.direction == dir_forward):
                motor.Move('backward', 'right')
            else:
                motor.Move('forward', 'right')
            self.turn = turn_right
            #print('turn right') # originally left
            self.count = 0
        # black(Dark)
        elif(left == 1 and middle == 1 and right == 1): # move backward
                motor.Move('backward', 'straight')
                self.direction = dir_forward
                self.turn = turn_no
                #print('Forward') # originally backward
                self.count = 0
        else: # move forward
            if(self.turn == turn_left):
                motor.Move('backward', 'right')
                self.previous_turn = turn_right
                self.count += 1
            elif(self.turn == turn_right):
                motor.Move('backward', 'left')
                self.previous_turn = turn_left
                self.count += 1
            else:
                motor.Move('backward', 'straight')
            self.direction = dir_forward
            #print('retracking', self.turn, self.count)
            #To-do: counts for Left/Right are different 
            if(self.count > 127000): # 127000 counts to rotate 360
                    self.turn = self.previous_turn
                    self.count = 0
            
                
            
            
    def __end__(self, motor):
        motor.__end__()
        print('end', self.count)
        
        
try:
    track = LineTrack(dir_forward, turn_no)
    motor = Motor(100) #move.setup()
    while 1:
        track.Run(motor)
except KeyboardInterrupt:
    track.__end__(motor)
