import RPi.GPIO as GPIO
import time

off = 1
on = 0  

class LED():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29,GPIO.OUT)
        GPIO.setup(31,GPIO.OUT)
        GPIO.setup(33,GPIO.OUT)
        
        GPIO.output(29,True)
        GPIO.output(31,True)
        GPIO.output(33,True)
        
        self.red = 29;
        self.green = 31;
        self.blue = 33;

        self.red_status = 0;
        self.green_status = 0;
        self.blue_status = 0;

    def is_ON(self, color):
        if(color == self.red):
            if(self.red_status == on):
                return on;
            else:
                return off;
        elif(color == self.green):
            if(self.green_status == on):
                return on;
            else:
                return off;
        elif(color == self.blue):
            if(self.blue_status == on):
                return on;
            else:
                return off;
        
    def turn_led(self, color):
        self.turn_allOFF()
        if(self.is_ON(color) == on): #on -> off
            GPIO.output(color,off)
            if(color == self.red):
                self.red_status = off
            elif(color == self.green):
                self.green_status = off
            else:
                self.blue_status = off
        else:
            GPIO.output(color,on)
            if(color == self.red):
                self.red_status = on
            elif(color == self.green):
                self.green_status = on
            else:
                self.blue_status = on
        
    def turn_allOFF(self):
        GPIO.output(29,True) # Red
        GPIO.output(31,True) # Green
        GPIO.output(33,True) # Blue
        
    def turn_allON(self):
        GPIO.output(29,False) # Red
        GPIO.output(31,False) # Green
        GPIO.output(33,False) # Blue
