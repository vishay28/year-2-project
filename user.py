#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
#Imports a package to do multithreading
from threading import Thread
#Imports the time package
import time

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

#A function that will constantly listen for messages being sent by the server
def serverListen():
    while True:
        #Listening for a message from the server
        serverMessage = server.recv(1024)
        #Decoding the message from the server
        serverMessage = serverMessage.decode()
        #Readting to different messages received from the server
        if serverMessage == "lightError":
            print(getTime() + "Light disconnected")
            serverMessage = ""
        elif serverMessage == "lightConnected":
            print(getTime() + "Light connected")
            serverMessage = ""
#A function to send the server a message
def serverMessageSend(message):
    server.send(message.encode())

#Creating a main method in which to run the program
if __name__ == "__main__":
    #Asking the user to input the ip of the server it is trying to connect to. (USE "localhost" if you are running the programs on the same computer)
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

    #Creating a thread to constantly listen to the
    serverListenThread = Thread(target=serverListen)
    #Starting the thread
    serverListenThread.start()

    #Setting the client ID and sending it to the server
    clientID = "user"
    serverMessageSend(clientID)

    #Creating a main loop in whcih the user can send messages to the server
    while True:
        #Resetting the user input
        userInput = ""
        #Getting the user input
        userInput = input()
        #Depending on what the user types different messages will be sent to the server
        if userInput == "on":
            serverMessageSend("switchOn")
        elif userInput == "off":
            serverMessageSend("switchOff")
        elif userInput == "red":
            serverMessageSend(userInput)
        elif userInput == "blue":
            serverMessageSend(userInput)
        elif userInput == "green":
            serverMessageSend(userInput)
        elif userInput == "purple":
            serverMessageSend(userInput)
        elif userInput == "yellow":
            serverMessageSend(userInput)
        elif userInput == "cyan":
            serverMessageSend(userInput)
        elif userInput == "white":
            serverMessageSend(userInput)
