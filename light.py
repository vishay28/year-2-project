#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime
#Importing the multithreading package
from threading import Thread
#Importing the time package
import time

#Setting the server message to blank
serverMessage = ""

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

#A function to constantly listen for messages from the server
def serverListen():
    #Creating a global variable in which to store the server message
    global serverMessage
    #Creating a while loop to constantly listen for messages
    while True:
        #Listening for messages from the server
        serverMessage = server.recv(1024)
        #Decoding the message received from the server
        serverMessage = serverMessage.decode()

#A function to remember which colour was last set
def rememberColour(colour):
    #Creating a global variable to strore the last colour set
    global lastColour
    #Assigning the variable to the last colour set
    lastColour = colour

#A function that will return the last colour that was set
def getLastColour():
    #Creating a global variable of lastColour
    global lastColour
    #Returning the last colour that was set
    return lastColour

#A function to print the colour that the light has switched to and then sending it to the rememberColour method
def lightSwitch(colour):
    print(getTime() + "Light switched to " + colour)
    rememberColour(colour)


#Creating a main method in which to run the program
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

    #Setting the client ID and sending it to the server
    clientID = "light"
    server.send(clientID.encode())

    #Creating a thread to constantly listen for server messages
    serverListenThread = Thread(target=serverListen)
    #Starting the thread
    serverListenThread.start()

    #Creating a global variable of the last colour variable
    global lastColour
    #Setting the default last colour to white
    lastColour = "white"

    #Creating a main loop in which the light will readct to the messages from the server
    while True:
        #Reacting to different messages sent from the server
        if serverMessage == "turnOn":
            print(getTime() + "Light turned on")
            #Getting the colour that was last set
            serverMessage = getLastColour()
        elif serverMessage == "turnOff":
            print(getTime() + "Light turned off")
            #GPIO pin 3 is red
            GPIO.set(3, GPIO.LOW)
            #GPIO pin 5, is blue
            GPIO.set(5, GPIO.LOW)
            #GPIO pin 7 is green
            GPIO.set(7, GPIO.LOW)
            serverMessage = ""
        if serverMessage == "red":
            GPIO.set(3, GPIO.HIGH)
            GPIO.set(5, GPIO.LOW)
            GPIO.set(7, GPIO.LOW)
            #Calling the function to print to the light log and to set the remember colour
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "blue":
            GPIO.set(3, GPIO.LOW)
            GPIO.set(5, GPIO.HIGH)
            GPIO.set(7, GPIO.LOW)
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "green":
            GPIO.set(3, GPIO.LOW)
            GPIO.set(5, GPIO.LOW)
            GPIO.set(7, GPIO.HIGH)
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "purple":
            GPIO.set(3, GPIO.HIGH)
            GPIO.set(5, GPIO.HIGH)
            GPIO.set(7, GPIO.LOW)
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "yellow":
            GPIO.set(3, GPIO.HIGH)
            GPIO.set(5, GPIO.LOW)
            GPIO.set(7, GPIO.HIGH)
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "cyan":
            GPIO.set(3, GPIO.LOW)
            GPIO.set(5, GPIO.HIGH)
            GPIO.set(7, GPIO.HIGH)
            lightSwitch(serverMessage)
            serverMessage = ""
        elif serverMessage == "white":
            GPIO.set(3, GPIO.HIGH)
            GPIO.set(5, GPIO.HIGH)
            GPIO.set(7, GPIO.HIGH)
            lightSwitch(serverMessage)
            serverMessage = ""

    serverListenThread.join()
