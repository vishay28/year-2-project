#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
from threading import Thread
import time

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime


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

    clientID = "user"
    server.send(clientID.encode())

    while True:
        userInput = ""
        message = ""
        userInput = input()
        if userInput == "on":
            message = "switchOn"
            server.send(message.encode())
        elif userInput == "off":
            message = "switchOff"
            server.send(message.encode())
        elif userInput == "red":
            message = "red"
            server.send(message.encode())
        elif userInput == "blue":
            message = "blue"
            server.send(message.encode())
        elif userInput == "green":
            message = "green"
            server.send(message.encode())