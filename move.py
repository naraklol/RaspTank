import time
import RPi.GPIO as GPIO

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 0
left_backward = 1

right_forward = 0
right_backward= 1

class Motor():
    
    def __init__(self, speed):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.Stop()
        
        # PWM(channel, frequency)
        self.pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        self.pwm_B = GPIO.PWM(Motor_B_EN, 1000) 
        
        self.pwm_A.start(speed)
        self.pwm_B.start(speed)
    
    def Stop(self):#Motor Stops
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)

    def Left(self, status, direction):#Motor 2 positive and negative rotation
        #self.pwm_B.start(0)
        if status == 0: # Stop
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
            #L298 Datasheet p.6
            #forward Pin2 high, Pin1 low
            #backward Pin2 low, Pin1 high
            if direction == Dir_backward:
                GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                #self.pwm_B.ChangeDutyCycle(self.speed)
            elif direction == Dir_forward:
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                #self.pwm_B.ChangeDutyCycle(self.speed)


    def Right(self, status, direction):#Motor 1 positive and negative rotation
        #self.pwm_A.start(0)
        if status == 0: # Stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if direction == Dir_forward:
                GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                #self.pwm_A.ChangeDutyCycle(self.speed)
            elif direction == Dir_backward:
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                #self.pwm_A.ChangeDutyCycle(self.speed)
        return direction


    def Move(self, direction, turn):  
        if direction == 'forward':
            if turn == 'right':
                self.Left(0, left_backward)
                self.Right(1, right_forward)
            elif turn == 'left':
                self.Left(1, left_forward)
                self.Right(0, right_backward)
            else:
                self.Left(1, left_forward)
                self.Right(1, right_forward)
        elif direction == 'backward':
            if turn == 'right':
                self.Left(0, left_forward)
                self.Right(1, right_backward)
            elif turn == 'left':
                self.Left(1, left_backward)
                self.Right(0, right_forward)
            else:
                self.Left(1, left_backward)
                self.Right(1, right_backward)
        elif direction == 'straight':
            if turn == 'right':
                self.Left(1, left_backward)
                self.Right(1, right_forward)
            elif turn == 'left':
                self.Left(1, left_forward)
                self.Right(1, right_backward)
            else:
                self.Stop()
        else:
            pass
        
    def __end__(self):
        self.Stop()
        GPIO.cleanup()             # Release resource

# Test Motor
'''
count = 0
motor = Motor(100) # This needs to be above 90 to keep both of the tires at the same speed
try:
    while 1:
        motor.Move('backward', 'straight')
except KeyboardInterrupt:
    motor.__end__()
'''
