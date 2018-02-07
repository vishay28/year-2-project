from generalFunctions import *


#A function that will constantly listen for messages being sent by the server
def serverListen():
    global lightConnected
    while True:
        #Listening for a message from the server
        serverMessage = server.recv(1024)
        #Decoding the message from the server
        serverMessage = serverMessage.decode()
        #Readting to different messages received from the server
        if serverMessage == "lightError":
            print(getTime() + "Light disconnected")
            #Setting the value of light connected to false
            lightConnected = False
            serverMessage = ""
        elif serverMessage == "lightConnected":
            print(getTime() + "Light connected")
            #Setting the value of light connected to true
            lightConnected = True
            serverMessage = ""
#A function to send the server a message
def serverMessageSend(message):
    server.send(message.encode())

#Creating a main method in which to run the program
if __name__ == "__main__":
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

    #Creating a thread to constantly listen to the
    serverListenThread = Thread(target=serverListen)
    #Starting the thread
    serverListenThread.start()

    #Setting the client ID and sending it to the server
    clientID = "user"
    serverMessageSend(clientID)

    #Defining a global variable to determine whether the light is connected or not
    global lightConnected
    #Setting the default value to true
    lightConnected = True

    #Creating a main loop in whcih the user can send messages to the server
    while True:
        #Resetting the user input
        userInput = ""
        #Getting the user input
        userInput = input()
        #Depending on what the user types different messages will be sent to the server
        #If the light is disconnected then don't allow the user to send a message to the server
        if lightConnected == False:
            print("Light disconnected")
        elif userInput == "on":
            serverMessageSend("switchOn")
        elif userInput == "off":
            serverMessageSend("switchOff")
        elif userInput in colourInputs:
            serverMessageSend(userInput)
