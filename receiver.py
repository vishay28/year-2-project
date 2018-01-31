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

client = socket.socket()
client.connect((ip,port))
print(getTime() + "Connected to " + ip)
print("Type on or off to switch the light on or off")
while True:
    message = ""
    switch = input()
    if switch == "on":
        message = "on"
        client.send(message.encode())
        print(getTime() + "Light turned on")
    elif switch == "off":
        message = "off"
        client.send(message.encode())
        print(getTime() + "Light turned off")
    else:
        print("That was not a valid input")
