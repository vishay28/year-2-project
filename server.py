from generalFunctions import *

#Setting the client message to blank
clientMessage = ""

#A function to send messages to the light client
def lightClientSendMessage(message):
    #Sending the message to the light client
    lightClient.send(message.encode())

#A function to send messages to the user client
def userClientSendMessage(message):
    #Sending the message to the light client
    userClient.send(message.encode())

#A function to constantly check if the light client is connected
def sendLightActive():
    #Creating a global variable to store whether the light error message has already been shown or not
    global lightMessageDisplayed
    #Creating a main loop in which the server will send the light client a message to check whether it is active
    while True:
        #Trying to send the light client a message
        try:
            #Waiting for a second before sending the next message
            time.sleep(1)
            #Attemting to send a message to the light client
            lightClientSendMessage("active")
        #A name error will occur if the the light client hasn't been initialised yet
        except NameError:
            #If this error occurs we just pass
            pass
        #A connection abort error or a connection reset error will occcur if the light client disconnects
        except (ConnectionAbortedError, ConnectionResetError):
            #Try to send the user a message letting it know that the light has been disconnected
            try:
                #Checking whether the error message for the light has already been displayed
                if lightMessageDisplayed == False:
                    #Printing to the server that the light has been disconnected
                    print(getTime() + "Light disconnected")
                    #The message has now been displayed so we can change the variable to true
                    lightMessageDisplayed = True
                    #Attempting to send the user client a message informing it of the light being disconnected
                    userClientSendMessage("lightError")
                    #Resetting the message to nothing
                    sendMessage=""
            #The connection reset error could occur here if the client disconnects first and then the light disconnects
            #The name error could occur here if the user client hasn't been initialised yet
            except (ConnectionResetError, NameError):
                #If this error occurs we just pass
                pass
            #If none of the above work then just pass
            pass

#A function to listen for a connecting device
def listenForDevice():
    #Creating a global varialble to store what the device type is
    global deviceType
    #Getting the server to listen for a device to connect to it
    while True:
        #Listening for a single device
        server.listen(1)
        #Accepting the incomming connection and getting the client name and address
        client1, client1Address = server.accept()
        #Listening for what the device ID is
        deviceType = client1.recv(1024)
        #Decoding the message received
        deviceType = deviceType.decode()
        #Passing the device ID, name and address to a function to determing which device it is
        determineDeviceType(deviceType, client1, client1Address)

#A function to determine which device has connected to the server
def determineDeviceType(clientID, client, clientAddress):
    #Assigning a global variables to all the clients and the booleans that determine whether their error message has been displayed
    global deviceType
    global switchClient
    global lightClient
    global userClient
    global lightMessageDisplayed
    global userMessageDisplayed
    global switchMessageDisplayed
    #Checking if the device ID is a switch
    if deviceType == "switch":
        #If it is a switch then printing to the server that the switch has connected
        print(getTime() + "Connected to switch " + str(clientAddress))
        #Assigning switchClient to the client that has just connected
        switchClient = client
        #Setting the error message displayed to false as the device has successfully connected back again so the error hasn't been shown yet
        switchMessageDisplayed = False
    #Checking if the device ID is a light
    elif deviceType == "light":
        #If it is a light then printing to the server that the light has connected
        print(getTime() + "Connected to light " + str(clientAddress))
        #Assigning lightClient to the client that has just connected
        lightClient = client
        #Setting the error message displayed to false as the device has successfully connected back again so the error hasn't been shown yet
        lightMessageDisplayed = False
        #Attempting to send the user client a message letting it know that the light has connected
        try:
            userClientSendMessage("lightConnected")
        #The name error may occur as the user client may not be initialised yet
        #the connection reset error could occur as the user may have also disconnected
        except (NameError, ConnectionResetError):
            #If the errors above occur then just pass
            pass
    #Checking if the device ID is a user
    elif deviceType == "user":
        #If it is a user then printing to the server that the user has connected
        print(getTime() + "Connected to user " + str(clientAddress))
        #Assigning userClient to the client that has just connected
        userClient = client
        #Setting the error message displayed to false as the device has successfully connected back again so the error hasn't been shown yet
        userMessageDisplayed = False

#A function to control the outputs based upon the switch status
def switchControl():
    #Creating the global variable to see what the clients are sending
    global clientMessage
    #Creating a global variable to check whether the error message for the switch has been displayed
    global switchMessageDisplayed

    #Creating a main loop in which the server can listen to the switch and respond to it
    while True:
        try:
            #This time delay has been added so that if the switch disconnects and then recoonects it doesn't display switch disconnected after it reconnecting
            time.sleep(0.1)

            #Listening for the switch and recieving any message that is being sent to the server
            clientMessage = switchClient.recv(1024)
            #Decoding the message that has been sent
            clientMessage = clientMessage.decode()

            #Determining what the switch message was and responding accordingly
            #If the switch sent the message to switch on
            if clientMessage == "switchOn":
                #Print that that the switch and the light have both been turned on
                print(getTime() + "Switch turned on")
                print(getTime() + "Light turned on")
                #Send a message to the light to switch on
                lightClientSendMessage("turnOn")
                #Resetting the message received
                clientMessage = ""
            #Print that that the switch and the light have both been turned off
            elif clientMessage == "switchOff":
                print(getTime() + "Switch turned off")
                print(getTime() + "Light turned off")
                #Send a message to the light to switch off
                lightClientSendMessage("turnOff")
                #Resetting the message received
                clientMessage = ""
        #This error may occur if the light client hasn't been initialised yet
        except NameError:
            #If the error above occurrs then just pass
            pass
        #This error may occur if the light client has disconnected
        except ConnectionResetError:
            #Checking if the switch error message has been displayed yet
            if switchMessageDisplayed == False:
                #If not then printing to the server that the switch has been disconnected
                print(getTime() + "Switch disconnected")
                #Changing the boolean so that the server knows it has already displayed the error message
                switchMessageDisplayed = True
            #If the error message has already been displayed then just pass
            pass

#A function to get the inputs from the user and send the right outputs
def userControl():
    #Creating a global variable to store the message received
    global clientMessage
    #Creating a global variable to store whether the user error message has been displayed
    global userMessageDisplayed
    #Creating a main loop in which the user can be controlled
    while True:
        try:
            #This time delay has been added so that if the user disconnects and then recoonects it doesn't display switch disconnected after it reconnecting
            time.sleep(0.1)
            #Setting the client message and send message to blank
            clientMessage = ""
            sendMessage = ""
            #Listening for the user to send a message
            clientMessage = userClient.recv(1024)
            #Decoding the message received
            clientMessage = clientMessage.decode()

            #Reacting to the messages received from the user
            if clientMessage == "switchOn":
                #Sending a message to the light to turn on
                lightClientSendMessage("turnOn")
                print(getTime() + "Light turned on")
            elif clientMessage == "switchOff":
                lightClientSendMessage("turnOff")
                print(getTime() + "Light turned off")
            elif clientMessage in colourInputs:
                lightClientSendMessage(clientMessage)
        #This error may occur if the light client or user client hasn't been initialised yet
        except NameError:
            #If this error occurs then just pass
            pass
        except ConnectionResetError:
        #Checking if the user error message has been displayed yet
            if userMessageDisplayed == False:
                #If not then printing to the server that the user has disconnected
                print(getTime() + "User disconnected")
                #Setting the boolean for the user error message displayed to true
                userMessageDisplayed = True
            #If it has already been displayed then just pass
            pass


#Creating a main function to run the program
if __name__ == "__main__":
    #Asking the user to set up the server by typing in the ip. (USE "localhost" if you are running the programs on the same computer)
    print("Input the server ip")
    #Getting the user input for the ip
    ip = input()

    #Asking the user to input a port for the server
    print("Input the port")
    #Getting the user input for the port and then coverting it to an integer
    port = int(input())

    #Defining a variable in which to open a socket
    server = socket.socket()
    #Binding the server socket to the ip and port
    server.bind((ip,port))

    #Creating a thread to listen for new devices trying to connect
    deviceListenThread = Thread(target=listenForDevice)
    #Creating a new thread to control the switch
    switchThread = Thread(target=switchControl)
    #Creating a new thread to control the user
    userThread = Thread(target=userControl)
    #Creating a new thread to constantly check if the light is still connected
    sendLightActiveThread = Thread(target=sendLightActive)

    #Starting all the threads
    deviceListenThread.start()
    switchThread.start()
    userThread.start()
    sendLightActiveThread.start()
