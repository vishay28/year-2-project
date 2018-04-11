#This program controls the smart plug device

#Imports the general file which contains various functions and variables which are used by multiple programs
from generalFunctions import *
#Importing the GPIO package
import RPi.GPIO as GPIO
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

#A function to listen for an incomming message from the server
def serverListen():
    #Defning the global variable for the server message
    global serverMessage
    #Creating a main loop to listen for server messages
    while True:
        #Listening for a message from the server
        serverMessage = server.recv(1024)
        #Decoding the message received by the server
        serverMessage = serverMessage.decode()


#Creating a main method in which to run the program
if __name__ == "__main__":
    #This waiting period has been introduced to ensure the Raspberry PI connects to the wifi before trying to connect to the server
    time.sleep(10)
    print(getTime() + "Plug initiated")
    #Setting up the GPIO pins to be in board mode
    GPIO.setmode(GPIO.BOARD)
    #Setting up the set pin
    GPIO.setup(3, GPIO.OUT)
    #Setting up the reset pin
    GPIO.setup(5, GPIO.OUT)

    #Connecting to the server
    server = connectToServer()

    #Defining the client ID
    clientID = "plug"
    #Letting the server know that a plug has connected
    server.send(clientID.encode())

    #Creating a thread to listen for messages from the server
    serverListenThread = Thread(target=serverListen)
    #Starting the thread
    serverListenThread.start()

    #Creating a main loop in which to run the program
    while True:
        #Checking what the server message is and responding accordingly
        if serverMessage == "turnOn":
            print(getTime() + "Plug turned on")
            #Pulsing the set pin
            GPIO.output(3, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(3, GPIO.LOW)
            serverMessage = ""
        elif serverMessage == "turnOff":
            print(getTime() + "Plug turned off")
            #Pulsing the reset pin
            GPIO.output(5, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(5, GPIO.LOW)
            serverMessage = ""
