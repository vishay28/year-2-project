#This program control the switch smart deivce

#Imports the general file which contains various functions and variables which are used by multiple programs
from generalFunctions import *
#Importing the GPIO package
import RPi.GPIO as GPIO


#A function to send the server a message
def serverMessageSend(message):
    #Sending the message to the server
    server.send(message.encode())

#Creating a method to constantly listen for server messages
def serverListen():
    #Setting the server message to blank
    serverMessage = ""
    #Creating a while loop to listen for messages from the server
    while True:
        #Listening for a message from the server
        serverMessage = server.recv(1024)
        #Decoding the message received
        serverMessage = serverMessage.decode()

#A main method to run the program
if __name__ == "__main__":
    #This waiting period has been introduced to ensure the Raspberry PI connects to the wifi before trying to connect to the server
    time.sleep(10)
    print(getTime() + "Switch initiated")
    #Setting up the GPIO pins to board mode
    GPIO.setmode(GPIO.BOARD)
    #Running the connect to server method
    server = connectToServer()

    #Setting the client ID and sending it to the server
    clientID = "switch"
    serverMessageSend(clientID)
    #Creating a thread to constantly listen for messages from the server
    serverListenThread = Thread(target=serverListen)
    #Starting the thread
    serverListenThread.start()
    #Setting up the GPIO pin
    GPIO.setup(3, GPIO.IN)
    # 1=off, 0=on
    #Setting the orginal state to off
    state = 1
    #Creating a main loop where the switch can provide inputs
    while True:
        time.sleep(0.5)
        #Sending the server a message depending on the switch state
        if ((GPIO.input(3)) == 0) and (state != 0):
            serverMessageSend("switchOn")
            state = 0
        elif ((GPIO.input(3)) == 1) and (state != 1):
            serverMessageSend("switchOff")
            state = 1
