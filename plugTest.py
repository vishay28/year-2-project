#Imports the general file which contains various functions and variables which are used by multiple programs
from generalFunctions import *

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
    print(getTime() + "Plug initiated")
    #Connecting to the server
    server = connectToServer()

    #Creatign a socket for the client to connect to the server
    server = socket.socket()

    #Trying to connect to the server using the ip and port specified by the user
    server.connect((ip,port))

    #Once successfully connected it prints a log of the date and time and the ip it has connected to
    print(getTime() + "Connected to " + ip)

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
            serverMessage = ""
        elif serverMessage == "turnOff":
            print(getTime() + "Plug turned off")
            serverMessage = ""
