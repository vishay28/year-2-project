from generalFunctions import *


#A function to send the server a message
def serverMessageSend(message):
    #Sending the message to the server
    server.send(message.encode())


#A main method to run the program
if __name__ == "__main__":
    server = connectToServer()

    #Setting the client ID and sending it to the server
    clientID = "switch"
    serverMessageSend(clientID)

    #Creating a main loop where the switch can provide inputs
    while True:
        #Resetting the user input
        userInput = ""
        #Getting the user input
        userInput = input()
        #Sending the server a message depending on the switch state
        if userInput == "on":
            serverMessageSend("switchOn")
        elif userInput == "off":
            serverMessageSend("switchOff")
