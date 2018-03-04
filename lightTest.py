from generalFunctions import *

#Setting the server message to blank
serverMessage = ""

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

#A function to print the colour that the light has switched to and then sending it to the rememberColour method
def lightSwitch(colour):
    if colour == "turnOff":
        print(getTime() + "Light switched off")
    else:
        print(getTime() + "Light switched to " + colour)
    if colour != "turnOff":
        rememberColour(colour)


#Creating a main method in which to run the program
if __name__ == "__main__":
    server = connectToServer()

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
            serverMessage = lastColour
        if serverMessage in colourInputs:
            #Calling the function to print to the light log and to set the remember colour
            lightSwitch(serverMessage)
            print(colourInputs[serverMessage][0])
            print(colourInputs[serverMessage][1])
            print(colourInputs[serverMessage][2])
            serverMessage=""

    serverListenThread.join()
