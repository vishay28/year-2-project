#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
import time
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

def sendLightActive():
    global lightMessageDisplayed
    while True:
        try:
            time.sleep(1)
            sendMessage = "active"
            lightClient.send(sendMessage.encode())
        except NameError:
            pass
        except ConnectionAbortedError:
            try:
                if lightMessageDisplayed == False:
                    sendMessage = "lightError"
                    print(getTime() + "Light disconnected")
                    lightMessageDisplayed = True
                    userClient.send(sendMessage.encode())
                    sendMessage=""
            except ConnectionResetError:
                pass
            pass

def listenForDevice():
    global deviceType
    #Getting the server to listen for a device to connect to it
    while True:
        server.listen(1)
        client1, client1Address = server.accept()
        deviceType = client1.recv(1024)
        deviceType = deviceType.decode()
        determineDeviceType(deviceType, client1, client1Address)

def determineDeviceType(clientID, client, clientAddress):
    global deviceType
    global switchClient
    global lightClient
    global userClient
    global lightMessageDisplayed
    global userMessageDisplayed
    global switchMessageDisplayed
    if deviceType == "switch":
        print(getTime() + "Connected to switch " + str(clientAddress))
        switchClient = client
        switchMessageDisplayed = False
    elif deviceType == "light":
        print(getTime() + "Connected to light " + str(clientAddress))
        lightClient = client
        lightMessageDisplayed = False
        try:
            sendMessage=("lightConnected")
            userClient.send(sendMessage.encode())
        except (NameError, ConnectionResetError):
            pass
    elif deviceType == "user":
        print(getTime() + "Connected to user " + str(clientAddress))
        userClient = client
        userMessageDisplayed = False

def switchControl():
    global clientMessage
    global switchMessageDisplayed

    while True:
        try:
            time.sleep(0.5)
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
        except NameError:
            pass
        except ConnectionResetError:
            if switchMessageDisplayed == False:
                print(getTime() + "Switch disconnected")
                switchMessageDisplayed = True
            pass

def userControl():
    global clientMessage
    global userMessageDisplayed
    while True:
        try:
            clientMessage = ""
            sendMessage = ""
            clientMessage = userClient.recv(1024)
            clientMessage = clientMessage.decode()

            if clientMessage == "switchOn":
                sendMessage = "turnOn"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned on")
            elif clientMessage == "switchOff":
                sendMessage = "turnOff"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned off")
            elif clientMessage == "red":
                sendMessage = "red"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to red")
            elif clientMessage == "blue":
                sendMessage = "blue"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to blue")
            elif clientMessage == "green":
                sendMessage = "green"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to green")
            elif clientMessage == "purple":
                sendMessage = "purple"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to purple")
            elif clientMessage == "yellow":
                sendMessage = "yellow"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to yellow")
            elif clientMessage == "cyan":
                sendMessage = "cyan"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to cyan")
            elif clientMessage == "white":
                sendMessage = "white"
                lightClient.send(sendMessage.encode())
                print(getTime() + "Light turned to white")
        except NameError:
            pass
        except ConnectionAbortedError:
            sendMessage = "lightError"
            userClient.send(sendMessage.encode())
            print(getTime() + "Light disconnected")
            sendMessage = ""
        except ConnectionResetError:
            if userMessageDisplayed == False:
                print(getTime() + "User disconnected")
                userMessageDisplayed = True
            pass



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

    deviceListenThread = Thread(target=listenForDevice)
    switchThread = Thread(target=switchControl)
    userThread = Thread(target=userControl)
    sendLightActiveThread = Thread(target=sendLightActive)

    deviceListenThread.start()
    switchThread.start()
    userThread.start()
    sendLightActiveThread.start()
