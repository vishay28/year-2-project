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
    global plugClient
    if deviceType == "switch":
        print(getTime() + "Connected to switch " + str(clientAddress))
        switchClient = client
    elif deviceType == "plug":
        print(getTime() + "Connected to plug " + str(clientAddress))
        plugClient = client
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
            print(getTime() + "Plug turned on")
            sendMessage = "turnOn"
            plugClient.send(sendMessage.encode())
            clientMessage = ""
        elif clientMessage == "switchOff":
            print(getTime() + "Switch turned off")
            print(getTime() + "Plug turned off")
            sendMessage = "turnOff"
            plugClient.send(sendMessage.encode())
            clientMessage = ""

def userControl():
    global clientMessage

    while True:
        clientMessage = switchClient.recv(1024)
        clientMessage = clientMessage.decode()

        if clientMessage == "switchOn":
            print(getTime() + "Switch turned on")
            print(getTime() + "Plug turned on")
            sendMessage = "turnOn"
            plugClient.send(sendMessage.encode())
            clientMessage = ""
        elif clientMessage == "switchOff":
            print(getTime() + "Switch turned off")
            print(getTime() + "Plug turned off")
            sendMessage = "turnOff"
            plugClient.send(sendMessage.encode())
            clientMessage = ""



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
    client3, client2Address = server.accept()
    deviceType = client3.recv(1024)
    deviceType = deviceType.decode()
    determineDeviceType(deviceType, client3, client3Address)

    switchThread = Thread(target=switchControl)
    userThread = Thread(target=userControl)

    switchThread.start()
    userThread.start()

    switchThread.join()
    userThread.join()
