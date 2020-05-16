import socket
import RPi.GPIO as GPIO

UDP_IP = "10.0.0.199"
UDP_PORT = 5005

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31,GPIO.OUT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

GPIO.output(31, False)

on = 1
off = 0
status = off

while True:
    data, addr = sock.recvfrom(1024)
    print 'received message:', data
    data = int(data)
    if(status == off):
        GPIO.output(data, True)
        status = on
    else:
        GPIO.output(data, False)
        status = off
    