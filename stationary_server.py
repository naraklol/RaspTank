# Echo server program
import socket

wrong = 29
correct = 33

red = 29
green = 31
blue = 33

HOST = '127.0.0.1'
PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)


data = ''
while 1:
    clientsocket,addr = s.accept()
    
    #check what data are received
    data = clientsocket.recv(1024)
    if(data.decode('ascii') != ''):
        print('data:', data, (data.decode('ascii')=='R'))

    #accepting color is set to RED for now
    if(data.decode('ascii') == 'R'):
        bytes_data = bytes(str(correct), encoding = 'ascii')
        print('bytes_data:', bytes_data)
        clientsocket.send(bytes_data)
    else:
        #otherwise(GREEN OR BLUE) will be considered to be wrong
        if(data.decode('ascii') != ''):
            bytes_data = bytes(str(wrong), encoding = 'ascii')
            print('bytes_data:', bytes_data)
            clientsocket.send(bytes_data)
        else:
            pass
s.close()