import socket
import os

wrong = 29
correct = 33

HOST = '127.0.0.1' #PC ip address
PORT = 5010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

data = ''
while 1:
    clientsocket,addr = s.accept()
    data = clientsocket.recv(1024)
    if(data.decode('ascii') != ''):
	answer = int(data, base=10)
        #print('data#1:', data, (int(data, base=10)==wrong))
        #print('data#2:', data, (int(data, base=10)==correct))
	if(answer == wrong):
	    os.startfile('wrong.mp3')
        elif(answer == right):
            os.startfile('right.mp3')

