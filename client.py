# Mobile Robot Client
import socket
from led import LED

HOST = '127.0.0.1'    #stationary robot ip address
PORT = 5005           

HOST_PC = '127.0.0.1' #pc ip address
PORT_PC = 5010

class Communication():
    def __init__(self):        
        #connect to the Stationary robot server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        self.enable = False
        self.message = ''

    def send(self, message):
        self.s.send(message.encode('ascii'))
        #self.clientsocket.send(message.encode('ascii'))

    def receive(self):
        data = self.s.recv(1024)
        #data = self.clientsocket.recv(1024)
        #data, addr = self.s.recvfrom(1024)
        print('data #1:',data)
        return (int(data, base=10))

    def connect_pc(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST_PC, PORT_PC))

    def set_enable(self, value):
        self.enable = value
    
    def get_enable_val(self):
        return self.enable

    def set_message(self, message):
        self.message = message
    
    def get_message(self):
        return self.message

    def __end__(self):
        self.s.close

#this needs to be merged with tracking_xxxx.py
try:
    led = LED()
    comm = Communication()

    #these set_enable and set_message are from camera
    #message needs to be 'R', 'B', 'G' string data
    #once camera detects the color, set the enable to true
    comm.set_enable(True)
    comm.set_message('R')

    data = ''

    #send the detected color to stationary robot
    #receive data = correct or wrong info
    #correct = 33(BLUE LED)
    #wrong = 29(RED LED)
    #disconnect with the server(reconnect whenever coming back to stationary)
    if(comm.get_enable_val()):
        comm.send(comm.get_message())
        data = comm.receive()
        comm.set_enable(False)
        comm.__end__()

    #depending on the answer, corresponding LED will turn on
    if(data == led.red or data == led.blue):
        print('data #3',data)
        led.turn_led(data)

        #connect to server and turn on the correct or wrong music
        comm.connect_pc()
        str_data = str(data)
        comm.send(str_data)
        comm.__end__()

except KeyboardInterrupt:
    comm.__end__()
    print('communication end')
