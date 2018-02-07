from threading import Thread
import datetime
import time
import socket

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

def connectToServer():
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
    return server

colourInputs = {"turnOff":[0,0,0],"red":[1,0,0], "blue":[0,1,0], "green":[0,0,1], "purple":[1,1,0], "yellow":[1,0,1], "cyan":[0,1,1], "white":[1,1,1]}
