#This program is impoted into most of the other programs as the functions defined in this class are common functions required by many programs
#Importing threading to allow the program to run multiple threads
from threading import Thread
#Importing the datetime function to allow the program to interact with the current date and time
import datetime
#Importing the time function to allow the program to wait for a specific amount of time
import time
#Importing the socket function to allow the program to interact with TCP sockets
import socket

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

#A function to connect to the server
def connectToServer():
    #Setting the ip address of the server to the fixed ip that the server was set up with
    ip = "192.168.0.10"
    #Setting the port number
    port = 5005
    #Creatign a socket for the client to connect to the server
    server = socket.socket()
    #Trying to connect to the server using the ip and port specified by the user
    server.connect((ip,port))
    #Once successfully connected it prints a log of the date and time and the ip it has connected to
    print(getTime() + "Connected to " + ip)
    #Returning the server information
    return server

#This array defines the GPIO outputs for different colours and states for the light
colourInputs = {"turnOff":[0,0,0],"red":[1,0,0], "blue":[0,1,0], "green":[0,0,1], "purple":[1,1,0], "yellow":[1,0,1], "cyan":[0,1,1], "white":[1,1,1]}
