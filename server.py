#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
from threading import Thread

clientMessage = ""

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

def determineDeviceType(clientID, client, clientAddress):
    global switchClient
    global lightClient
    global userClient
    if deviceType == "switch":
        print(getTime() + "Connected to switch " + str(clientAddress))
        switchClient = client
    elif deviceType == "light":
        print(getTime() + "Connected to light " + str(clientAddress))
        lightClient = client
    elif deviceType == "user":
        print(getTime() + "Connected to user " + str(clientAddress))
        userClient = client

def switchControl():
    global clientMessage

    while True:
        clientMessage = switchClient.recv(1024)
        clientMessage = clientMessage.decode()

        if clientMessage == "switchOn":
            print(getTime() + "Switch turned on")
            print(getTime() + "Light turned on")
            sendMessage = "turnOn"
            lightClient.send(sendMessage.encode())
            clientMessage = ""
        elif clientMessage == "switchOff":
            print(getTime() + "Switch turned off")
            print(getTime() + "Light turned off")
            sendMessage = "turnOff"
            lightClient.send(sendMessage.encode())
            clientMessage = ""

def userControl():
    global clientMessage

    while True:
        clientMessage = ""
        sendMessage = ""
        clientMessage = userClient.recv(1024)
        clientMessage = clientMessage.decode()

        if clientMessage == "switchOn":
            print(getTime() + "Switch turned on")
            print(getTime() + "Light turned on")
            sendMessage = "turnOn"
            lightClient.send(sendMessage.encode())
        elif clientMessage == "switchOff":
            print(getTime() + "Switch turned off")
            print(getTime() + "Light turned off")
            sendMessage = "turnOff"
            lightClient.send(sendMessage.encode())
        elif clientMessage == "red":
            print(getTime() + "Light turned to red")
            sendMessage = "red"
            lightClient.send(sendMessage.encode())
        elif clientMessage == "blue":
            print(getTime() + "Light turned to blue")
            sendMessage = "blue"
            lightClient.send(sendMessage.encode())
        elif clientMessage == "green":
            print(getTime() + "Light turned to green")
            sendMessage = "green"
            lightClient.send(sendMessage.encode())




if __name__ == "__main__":
    #Asking the user to set up the server by typing in the ip. (USE "localhost" if you are running both programs on the same computer)
    print("Input the server ip")
    #Getting the user input for the ip
    ip = input()

    #Asking the user to input a port for the server
    print("Input the port")
    #Getting the user input for the port and then coverting it to an integer
    port = int(input())

    #Defining a variable in which to open a socket
    server = socket.socket()
    #Binding the server socket to the ip and port
    server.bind((ip,port))

    #Getting the server to listen for a device to connect to it
    server.listen(1)
    client1, client1Address = server.accept()
    deviceType = client1.recv(1024)
    deviceType = deviceType.decode()
    determineDeviceType(deviceType, client1, client1Address)


    server.listen(1)
    client2, client2Address = server.accept()
    deviceType = client2.recv(1024)
    deviceType = deviceType.decode()
    determineDeviceType(deviceType, client2, client2Address)

    server.listen(1)
    client3, client3Address = server.accept()
    deviceType = client3.recv(1024)
    deviceType = deviceType.decode()
    determineDeviceType(deviceType, client3, client3Address)

    switchThread = Thread(target=switchControl)
    userThread = Thread(target=userControl)

    switchThread.start()
    userThread.start()

    switchThread.join()
    userThread.join()
