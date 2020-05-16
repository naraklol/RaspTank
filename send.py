import socket
import RPi.GPIO as GPIO

UDP_IP = "10.0.0.199"
UDP_PORT = 5005
MESSAGE = '31'
BYTES_MESSAGE = bytes(MESSAGE, encoding = 'utf-8')

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(BYTES_MESSAGE, (UDP_IP, UDP_PORT))
#sock.sendall(MESSAGE.encode('utf-8'))