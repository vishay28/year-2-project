import socket
import datetime

def getTime():
    currentTime = str(datetime.datetime.now())
    currentTime = (currentTime[0:19] + ": ")
    return currentTime

print("Input the server ip")
ip = input()
print("Input the port")
port = int(input())

server = socket.socket()
server.bind((ip,port))
server.listen(1)
receiver, address = server.accept()

print(getTime() + "Connected to " + str(address))

origMessage = None
message = None

while True:
    message = receiver.recv(1024)
    message = message.decode()
    if (message is not None) & (message is not origMessage):
        origMessage = message
        if message == "on":
            print(getTime() + "Light turned on")
        if message == "off":
            print(getTime() + "Light turned off")
