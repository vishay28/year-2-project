#This program controls all the smart devices

#Imports the general file which contains various functions and variables which are used by multiple programs
from generalFunctions import *
#Imports the pymongo package which allows python to interact with the mongoDB database
import pymongo

#Setting the client message to blank
clientMessage = ""
#Setting the counters to 1
switchCount = 1
lightCount = 1
plugCount = 1

#Creating a blank dictionary to store the socket information of all the devices that connect
deviceClient = {}

#A function to allow for autonomous turning on and off of devices
def timeCheck():
    #Assigning a variable to the plug and light tables
    plugsCollection = devicesDB.plug
    lightsCollection = devicesDB.lightBulb
    #Creating a main loop in which to run the program
    while True:
        while True:
            time.sleep(0.5)
            #Get the current time
            currentTime = str(datetime.datetime.now())
            #Selecting only the information that we want to display
            currentTime = (currentTime[17:19])
            #Check if the time is on the minute
            if currentTime == "00":
                #Assigning a dictionary to the light table
                lightsDict = devicesDB.lightBulb.find({})
                #For each row in the table
                for document in lightsDict:
                    #Get the data for the row
                    documentData = devicesDB.lightBulb.find_one({"ident": document["ident"]})

                    #Assigning an array to the the times that the user wants to turn the light on
                    onTimeArray = documentData["onTimes"]
                    #For each element in the array
                    for onTime in onTimeArray:
                        #Get the current time
                        currentTime = str(datetime.datetime.now())
                        currentTime = (currentTime[11:16])
                        #If the current time is equal to the element within the array
                        if onTime == currentTime:
                            #Set that light to on
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'r': 255}})
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'g': 255}})
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'b': 255}})

                    #Sane as above just for off times instead
                    offTimeArray = documentData["offTimes"]
                    for offTime in offTimeArray:
                        currentTime = str(datetime.datetime.now())
                        currentTime = (currentTime[11:16])
                        if offTime == currentTime:
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'r': 0}})
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'g': 0}})
                            lightsCollection.update_one({'ident': document["ident"]}, {'$set': {'b': 0}})

                #Same as above just for plugs instead
                plugsDict = devicesDB.plug.find({})
                for document in plugsDict:
                    documentData = devicesDB.plug.find_one({"ident": document["ident"]})

                    onTimeArray = documentData["onTimes"]
                    for onTime in onTimeArray:
                        currentTime = str(datetime.datetime.now())
                        currentTime = (currentTime[11:16])
                        if onTime == currentTime:
                            plugsCollection.update_one({'ident': document["ident"]}, {'$set': {'state': 1}})

                    offTimeArray = documentData["offTimes"]
                    for offTime in offTimeArray:
                        currentTime = str(datetime.datetime.now())
                        currentTime = (currentTime[11:16])
                        if offTime == currentTime:
                            plugsCollection.update_one({'ident': document["ident"]}, {'$set': {'state': 0}})

                    time.sleep(1)


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
    #Calling the global variable of the deviceClient dictionary
    global deviceClient
    #Calling the global variable for the counters for the devices
    global switchCount
    global lightCount
    global plugCount
    #Creating a global variable for the user program
    global userClient
    #Checking if the device ID is a switch
    if deviceType == "switch":
        #Creating a name for the switch by taking the counter value
        clientName = ("switch" + str(switchCount))
        #Assigning the client name to the socket information within the dictionary
        deviceClient[clientName] = client
        #Assigning a variable to the switch collection in the database
        switchesCollection = devicesDB.switch
        #Creating a document within the database with the switch's data
        document = {"ident": clientName,"name": clientName, "slaveid": "", "state": 0}
        #Inserting the document into the database
        switchesCollection.insert_one(document)
        #Printing to the server the name and address of the device that has connected
        print(getTime() + "Connected to " + clientName + " " + str(clientAddress))
        #Creating a thread to listen to the connected switch
        aThread = Thread(target=switchControl, args=(clientName,))
        #Starting the thread
        aThread.start()
        #Incrimenting the counter for the switch
        switchCount = switchCount+1
    #Checking if the device ID is a light
    elif deviceType == "light":
        #Creating a name for the light by taking the counter value
        clientName = ("light" + str(lightCount))
        #Assigning the client name to the socket information within the dictionary
        deviceClient[clientName] = client
        #Assigning a variable to the lightBulb collection in the database
        lightCollection = devicesDB.lightBulb
        #Creating a document within the database with the light's data
        document = {"ident": clientName,"name": clientName, "r": 0, "g": 0, "b": 0, "onTimes": [], "offTimes": [],}
        #Inserting the document into the database
        lightCollection.insert_one(document)
        #Printing to the server the name and address of the device that has connected
        print(getTime() + "Connected to " + clientName + " " + str(clientAddress))
        #Incrimenting the counter for the light
        lightCount = lightCount+1
    #Checking if the device ID is the user program
    elif deviceType == "user":
        #If it is a user then printing to the server that the user has connected
        print(getTime() + "Connected to user " + str(clientAddress))
        #Assigning userClient to the client that has just connected
        userClient = client
    #Checking if the device ID is a plug
    elif deviceType == "plug":
        #Creating a name for the plug by taking the counter value
        clientName = ("plug" + str(plugCount))
        #Assigning the client name to the socket information within the dictionary
        deviceClient[clientName] = client
        #Assigning a variable to the plug collection in the database
        plugCollection = devicesDB.plug
        #Creating a document within the database with the plug's data
        document = {"ident": clientName,"name": clientName, "state": 0, "onTimes": [], "offTimes": [],}
        #Inserting the document into the database
        plugCollection.insert_one(document)
        #Printing to the server the name and address of the device that has connected
        print(getTime() + "Connected to " + clientName + " " + str(clientAddress))
        #Incrimenting the counter for the plug
        plugCount = plugCount+1

#A function to control the outputs based upon the switch status
def switchControl(name):
    #Calling the global variable to see what the clients are sending
    global clientMessage
    #Assigning a variable to the switch collection in the database
    switchesCollection = devicesDB.switch
    plugsCollection = devicesDB.plug
    lightsCollection = devicesDB.lightBulb

    #Creating a main loop in which the server can listen to the switch and respond to it
    while True:
        try:
            #This time delay has been added so that if the switch disconnects and then reconnects it doesn't display switch disconnected after it reconnecting
            time.sleep(0.1)

            #Listening for the switch and recieving any message that is being sent to the server
            clientMessage = (deviceClient[name]).recv(1024)
            #Decoding the message that has been sent
            clientMessage = clientMessage.decode()
            #Getting the document for the switch
            switchData = devicesDB.switch.find_one({"ident": name})
            #Getting the slaveid from the document
            slaveID = switchData["slaveid"]
            #Assigning a variable to the socket of the slaveid
            slaveClient = deviceClient[slaveID]

            #Determining what the switch message was and responding accordingly
            #If the switch is switched on
            if clientMessage == "switchOn":
                #Print the name of the switch and that it was turned on
                print(getTime() + name + " turned on")
                #Update the document to set the switch state to on
                switchesCollection.update_one({'ident': name}, {'$set': {'state': 1}})
                if "plug" in slaveID:
                    plugsCollection.update_one({'ident': slaveID}, {'$set': {'state': 1}})
                elif "light" in slaveID:
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'r': 255}})
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'g': 255}})
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'b': 255}})
                #Print the slaveid and that it was turned on
                print(getTime() + slaveID + " turned on")
                #Resetting the message received
                clientMessage = ""
            #If the switch is switched off
            elif clientMessage == "switchOff":
                #Print the name of the switch and that it was turned off
                print(getTime() + name + " turned off")
                #Update the document to set the switch state to off
                switchesCollection.update_one({'ident': name}, {'$set': {'state': 0}})
                if "plug" in slaveID:
                    plugsCollection.update_one({'ident': slaveID}, {'$set': {'state': 0}})
                elif "light" in slaveID:
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'r': 0}})
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'g': 0}})
                    lightsCollection.update_one({'ident': slaveID}, {'$set': {'b': 0}})
                #Print the slaveid and that it was turned off
                print(getTime() + slaveID + " turned off")
                #Resetting the message received
                clientMessage = ""
        #This error may occur if the switch client hasn't been initialised yet
        except (NameError, KeyError):
            #If the error above occurrs then just pass
            pass
        #This error may occur if the switch or plug client has disconnected
        except (ConnectionResetError, ConnectionAbortedError, TimeoutError):
            #Printing which device has disconnected
            print(getTime() + name + " disconnected")
            #Determining whether it was a switch or a plug that disconnected
            if "switch" in name:
                #Deleting the device from the database
                devicesDB.switch.delete_many({"ident": name})
            elif "plug" in name:
                #Deleting the device from the database
                devicesDB.plug.delete_many({"ident": name})
            #Deleting the device from the dictionary storing the socket information
            del deviceClient[name]

#A function to send messages to the light client
def lightClientSendMessage(deviceid, message):
    #Calling the global variable for the deviceClient dictionary
    global deviceClient
    #Assigning a variable to the lightBulb collection stored in the database
    lightsCollection = devicesDB.lightBulb
    #Sending the message to the light client
    while True:
            try:
                #Sending the message to the light client
                deviceClient[deviceid].send(message.encode())
                #Determining what the message was and then updating the database accordingly
                if message == "turnOn":
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'r': 255}})
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'g': 255}})
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'b': 255}})
                    #Printing to the server the ID of the light and that it was turned on
                    print(getTime() + deviceid + " turned on")
                elif message == "turnOff":
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'r': 0}})
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'g': 0}})
                    lightsCollection.update_one({'ident': deviceid}, {'$set': {'b': 0}})
                    #Printing to the server the ID of the light and that it was turned off
                    print(getTime() + deviceid + " turned off")
            #This error will occur if the light disconnects
            except (ConnectionResetError, ConnectionAbortedError):
                #Print to the server the device that has disconnected
                print(getTime() + deviceid + " disconnected")
                #Deleting the light from the database
                devicesDB.lightBulb.delete_many({"ident": deviceid})
                #Deleting the light from the dictionary that stores the socket information
                del deviceClient[deviceid]
            #Breaking the loop
            break

#Creating a function to send a plug a message
def plugSendMessage(deviceid, message):
    #Assigning a variable to the plug collection in the database
    plugsCollection = devicesDB.plug
    #Creating a main loop in which to send the message
    while True:
        try:
            #Sending the message to the specified plug
            deviceClient[deviceid].send(message.encode())
            #Determining what the message was
            if message == "turnOn":
                #Updating the document in the database
                plugsCollection.update_one({'ident': deviceid}, {'$set': {'state': 1}})
                print(getTime() + deviceid + " turned on")
            elif message == "turnOff":
                #Updating the document in the database
                plugsCollection.update_one({'ident': deviceid}, {'$set': {'state': 0}})
                print(getTime() + deviceid + " turned off")
        #This error will occur if the plug disconnects
        except (ConnectionResetError, ConnectionAbortedError):
            #Printing to the server which plug was disconnected
            print(getTime() + deviceid + " disconnected")
            #Deleting the plug from the database
            devicesDB.plug.delete_many({"ident": deviceid})
            #Deleting the plug from the dictionary that stores the socket information
            del deviceClient[deviceid]
        #Breaking the loop
        break

#A function to check whether any of the lights have disconnected
def lightActive():
    #Creating a main loop
    while True:
        #Having a 2 second time delay
        time.sleep(2)
        try:
            #Iterating through all the items in the database
            for i, j in deviceClient.items():
                #If any of them are lights
                if "light" in i:
                    #Send a message to the light to check if it is still active
                    lightClientSendMessage(i, "active")
        #This error will occur if the light has disconnected
        except ConnectionResetError:
            #Print which light has disconnected
            print(getTime() + i + " disconnected")
            #Deleting the light from the database
            devicesDB.lightBulb.delete_many({"ident": i})
            #Deleting the light from the dictionary that stores the socket information
            del deviceClient[i]
        #This error will occur because the size of the dictionary will change
        except RuntimeError:
            #If the above error occurs then just pass
            pass

#A function to check whether any of the plugs have disconnected
def plugActive():
    #Creating a main loop
    while True:
        #Having a 2 second time delay
        time.sleep(2)
        try:
            #Iterating through all the items in the database
            for i, j in deviceClient.items():
                #If any of them are plugs
                if "plug" in i:
                    #Send a message to the plug to check if it is still active
                    plugSendMessage(i, "active")
        #This error will occur if the plug has disconnected
        except ConnectionResetError:
            #Print which plug has disconnected
            print(getTime() + i + " disconnected")
            #Deleting the plug from the database
            devicesDB.plug.delete_many({"ident": i})
            #Deleting the plug from the dictionary that stores the socket information
            del deviceClient[i]
        #This error will occur because the size of the dictionary will change
        except RuntimeError:
            #If the above error occurs then just pass
            pass

#A function to check whether any of the plugs have disconnected
def switchActive():
    #Creating a main loop
    while True:
        #Having a 2 second time delay
        time.sleep(2)
        try:
            #Iterating through all the items in the database
            for i, j in deviceClient.items():
                #If any of them are plugs
                if "switch" in i:
                    #Send a message to the switch to check if it is still active
                    switchSendMessage(i, "active")
        #This error will occur if the switch has disconnected
        except ConnectionResetError:
            #Print which switch has disconnected
            print(getTime() + i + " disconnected")
            #Deleting the switch from the database
            devicesDB.switch.delete_many({"ident": i})
            #Deleting the switch from the dictionary that stores the socket information
            del deviceClient[i]
        #This error will occur because the size of the dictionary will change
        except RuntimeError:
            #If the above error occurs then just pass
            pass

#A fuction to send a message to a specific switch
def switchSendMessage(deviceid, message):
    try:
        #Sending a message to the specified switch
        deviceClient[deviceid].send(message.encode())
    #This error will occur if the switch has disconnected
    except (ConnectionResetError, ConnectionAbortedError):
        #Print which switch has disconnected
        print(getTime() + deviceid + " disconnected")
        #Deleting the switch from the database
        devicesDB.switch.delete_many({"ident": deviceid})
        #Deleting the switch from the dictionary that stores the socket information
        del deviceClient[deviceid]

#A function to get the inputs from the user and send the right outputs
def userControl():
    #Calling the global variable for the user client
    global userClient
    #Defining all the variables
    newMessage = ""
    clientMessage = ""
    newDeviceid = ""
    deviceid = ""
    deviceStatus = {}
    #Creating a main loop in which the user can be controlled
    while True:
        try:
            #This time delay has been added so that if the user disconnects and then recoonects it doesn't display switch disconnected after it reconnecting
            time.sleep(0.1)
            #Setting the client message and send message to blank
            sendMessage = ""
            #Listening for the user to send a message
            deviceid = userClient.recv(1024)
            #Decoding the message received
            deviceid = deviceid.decode()
            #This time delay has been added so that the deviceid and message don't get mixed up
            time.sleep(0.1)
            clientMessage = userClient.recv(1024)
            #Decoding the message received
            clientMessage = clientMessage.decode()

            #Checking if the device status has already been added to the dictionary
            #This prevents duplicate messages being sent
            if deviceid not in deviceStatus:
                #Adding the device and it's device status to the dictionary
                deviceStatus[deviceid] = clientMessage
            #Checking which client sent the message and what the message was and responding to it
            if (deviceStatus[deviceid] != clientMessage):
                if (("light" in deviceid) and (clientMessage == "switchOff")):
                    lightClientSendMessage(deviceid, "turnOff")
                    deviceStatus[deviceid] = clientMessage
                elif (("light" in deviceid) and (clientMessage in colourInputs)):
                    print("Light switched to " + clientMessage)
                    lightClientSendMessage(deviceid, clientMessage)
                    deviceStatus[deviceid] = clientMessage
                elif (("plug" in deviceid) and (clientMessage == "turnOn")):
                    plugSendMessage(deviceid, clientMessage)
                    deviceStatus[deviceid] = clientMessage
                elif (("plug" in deviceid) and (clientMessage == "turnOff")):
                    plugSendMessage(deviceid, clientMessage)
                    deviceStatus[deviceid] = clientMessage
        #This error may occur if the light client or user client hasn't been initialised yet
        except (NameError, ConnectionResetError):
            #If this error occurs then just pass
            pass

#Creating a main function to run the program
if __name__ == "__main__":
    print(getTime() + "Server initiated")
    ip = "192.168.0.10"
    port = 5005

    #Defining a variable in which to open a socket
    server = socket.socket()
    #Binding the server socket to the ip and port
    server.bind((ip,port))

    #Connecting to the database
    databaseClient = pymongo.MongoClient("localhost", 27017)
    devicesDB = databaseClient.weblightDatabase

    #Creating a thread to listen for new devices trying to connect and threads to check if the devices are still active
    deviceListenThread = Thread(target=listenForDevice)
    userThread = Thread(target=userControl)
    lightActiveThread = Thread(target=lightActive)
    plugActiveThread = Thread(target=plugActive)
    switchActiveThread = Thread(target=switchActive)
    timeCheckThread = Thread(target=timeCheck)

    #Starting all the threads
    deviceListenThread.start()
    userThread.start()
    lightActiveThread.start()
    plugActiveThread.start()
    switchActiveThread.start()
    timeCheckThread.start()
