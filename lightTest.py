from data import *

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
            serverMessage = lastColour
        if serverMessage in colourInputs:
            #Calling the function to print to the light log and to set the remember colour
            lightSwitch(serverMessage)
            print(colourInputs[serverMessage][0])
            print(colourInputs[serverMessage][1])
            print(colourInputs[serverMessage][2])
            serverMessage=""

    serverListenThread.join()
