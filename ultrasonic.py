import RPi.GPIO as GPIO
import time

class Ultrasonic():
    def __init__(self):
        self.tx_pin = 11
        self.rx_pin = 8

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.tx_pin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.rx_pin, GPIO.IN)

    def check_distance(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.tx_pin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.rx_pin, GPIO.IN)
        GPIO.output(self.tx_pin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.tx_pin, GPIO.LOW)
        while not GPIO.input(self.rx_pin):
            pass
        t1 = time.time()
        while GPIO.input(self.rx_pin):
            pass
        t2 = time.time()
        return round((t2-t1)*340/2,2)

if __name__ == '__main__':
    ultra = Ultrasonic()
    while 1:
        dist = ultra.check_distance()
        print("Distance is", dist, end='\r')
