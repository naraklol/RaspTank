import time
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
        
#################################################
# Setting Max and Min movements of the Servo
# This seems to work the best
#################################################
servo15_init = 300
servo15_open = 200
servo15_close = 290 # when claws are tight, the robot reboots 

servo13_init = 300
servo13_up = 200 
servo13_down = 375

servo12_init = 300
servo12_up = 350 
servo12_down = 175

#################################
# Setting the Servos base
# servo_degree is adjustable
#################################
claw_angle = 10
servo_degree = 25


class Servo():
    def __init__(self):
        pwm.set_pwm(12,0,servo12_init)
        pwm.set_pwm(13,0,servo13_init)
        pwm.set_pwm(15,0,servo15_init)
        time.sleep(1)
        
        self.servo12_curval = servo12_init
        self.servo13_curval = servo13_init
        self.servo15_curval = servo15_init
    
    def open_claws(self):
        while(self.servo15_curval > servo15_open):
            self.servo15_curval -= claw_angle
            pwm.set_pwm(15,0,self.servo15_curval)
            time.sleep(1)
        print("SERVO 15 open done", self.servo15_curval)
    
    def close_claws(self):
        while(self.servo15_curval < servo15_close):
            self.servo15_curval += claw_angle
            pwm.set_pwm(15,0,self.servo15_curval)
            time.sleep(1)
        print("SERVO 15 close done", self.servo15_curval)
    
   
    def lower_arm(self, step):
        if((self.servo13_curval + (step * servo_degree)) > servo13_down):
            servo13_max = servo13_down
        else:
            servo13_max = self.servo13_curval + (step * servo_degree)
                
        while(self.servo13_curval < servo13_max):
            self.servo13_curval += servo_degree
            pwm.set_pwm(13,0,self.servo13_curval)
            time.sleep(1)
        #print("SERVO 13 down done", self.servo13_curval)
    
    
    def lift_arm(self, step):
        if((self.servo13_curval - (step * servo_degree)) < servo13_up):
            servo13_min = servo13_up
        else:
            servo13_min = self.servo13_curval - (step * servo_degree)
                
        while(self.servo13_curval > servo13_min):
            self.servo13_curval -= servo_degree
            pwm.set_pwm(13,0,self.servo13_curval)
            time.sleep(1)
        #print("SERVO 13 up done", self.servo13_curval)
    
    
    def lower_base(self, step):
        if((self.servo12_curval - (step * servo_degree)) < servo12_down):
            servo12_min = servo12_down
        else:
            servo12_min = self.servo12_curval - (step * servo_degree)
                
        while(self.servo12_curval > servo12_min):
            self.servo12_curval -= servo_degree
            pwm.set_pwm(12,0,self.servo12_curval)
            time.sleep(1)
        print("SERVO 12 down done", self.servo12_curval)
    
    def lift_base(self, step):
        if((self.servo12_curval + (step * servo_degree)) > servo12_up):
            servo12_max = servo12_up
        else:
            servo12_max = self.servo12_curval + (step * servo_degree)
            
        while(self.servo12_curval < servo12_max):
            self.servo12_curval += servo_degree
            pwm.set_pwm(12,0,self.servo12_curval)
            time.sleep(1)
        print("SERVO 12 up done", self.servo12_curval)

    def pickup(self):
        self.open_claws()
        
        # Lower the claws
        self.lift_arm(1)
        self.lower_base(5)
        
        # grab the object
        self.close_claws()
        self.lift_base(3)
        self.lower_arm(1)

    def drop(self):
        # drop the object
        self.lift_arm(1)
        self.lower_base(3)
        self.open_claws()

        self.close_claws()
        self.lift_base(3)
        self.lower_arm(1)

'''
servo = Servo()

servo.open_claws()

# Lower the claws
servo.lift_arm(1)
servo.lower_base(3)
servo.lift_arm(1)
servo.lower_base(2)
servo.close_claws()

# Lift the claws
#pwm.set_pwm_freq(50)
servo.lift_base(4)
'''