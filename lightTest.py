#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
from threading import Thread
import time

serverMessage = ""

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

def serverListen():
    global serverMessage
    while True:
        serverMessage = server.recv(1024)
        serverMessage = serverMessage.decode()

def rememberColour(colour):
    global redColour
    global blueColour
    global greenColour
    global purpleColour
    global yellowColour
    global cyanColour
    global whiteColour
    redColour = False
    blueColour = False
    greenColour = False
    purpleColour = False
    yellowColour = False
    cyanColour = False
    whiteColour = False
    if colour == "red":
        redColour = True
    elif colour == "blue":
        blueColour = True
    elif colour == "green":
        greenColour = True
    elif colour == "purple":
        purpleColour = True
    elif colour == "yellow":
        yellowColour = True
    elif colour == "cyan":
        cyanColour = True
    elif colour == "white":
        whiteColour = True

def lightSwitch(colour):
    print(getTime() + "Light switched to " + colour)
    rememberColour(colour)



if __name__ == "__main__":
    #Asking the user to input the ip of the server it is trying to connect to. (USE "localhost" if you are running both programs on the same computer)
    print("Input the server ip")
    #Getting the user input for the ip
    ip = input()

    #Asking the user to input the port of the server it is trying to connect to
    print("Input the port")
    #Getting the user input for the port and then coverting it to an integer
    port = int(input())

    #Creatign a socket for the client to connect to the server
    server = socket.socket()

    #Trying to connect to the server using the ip and port specified by the user
    server.connect((ip,port))

    #Once successfully connected it prints a log of the date and time and the ip it has connected to
    print(getTime() + "Connected to " + ip)

    clientID = "light"
    server.send(clientID.encode())

    serverListenThread = Thread(target=serverListen)
    serverListenThread.start()

    redColour = False
    blueColour = False
    greenColour = False
    purpleColour = False
    yellowColour = False
    cyanColour = False
    whiteColour = True

    while True:
        if serverMessage == "turnOn":
            print(getTime() + "Light turned on")
            if redColour == True:
                serverMessage = "red"
            elif blueColour == True:
                serverMessage = "blue"
            elif greenColour == True:
                serverMessage = "green"
            elif purpleColour == True:
                serverMessage = "purple"
            elif yellowColour == True:
                serverMessage = "yellow"
            elif cyanColour == True:
                serverMessage = "cyan"
            elif whiteColour == True:
                serverMessage = "white"
        elif serverMessage == "turnOff":
            print(getTime() + "Light turned off")
            serverMessage = ""
        if serverMessage == "red":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "blue":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "green":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "purple":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "yellow":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "cyan":
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "white":
            lightSwitch(serverMessage)
            serverMessage = ""

    serverListenThread.join()
