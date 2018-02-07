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

colourInputs = {"turnOff":[0,0,0],"red":[1,0,0], "blue":[0,1,0], "green":[0,0,1], "purple":[1,1,0], "yellow":[1,0,1], "cyan":[0,1,1], "white":[1,1,1]}
