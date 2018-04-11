#This program interacts with the database and feedsback to the server program

#Importing the generalFunctions file
from generalFunctions import *
#Importing pymongo in order to interact with the database
import pymongo


#A function to send the server a message
def serverMessageSend(message):
    #Sending a messge to the server
    server.send(message.encode())

#Afunction to convert the RGB values from the web interface to binary
def convertToBinary(num):
    #Setting the value of binary to 0
    binary = 0
    if num>=128:
        binary = 1
    elif num<128:
        binary = 0
    return binary

#A function to check what state the light should be on from the database
def lightCheck():
    #Setting the values to blank
    newMessage = ""
    message = ""

    #Creating a main loop in whcih the user can send messages to the server
    while True:
        #Getting the information from the light table in the database
        lightsDict = devicesDB.lightBulb.find({})
        try:
            #For each light in the database the program will iterate through it and check it's status
            for document in lightsDict:
                #Gets the program to sleep for one second
                time.sleep(1)
                #Getting the RGB values for the light
                RGBValues = devicesDB.lightBulb.find_one({"ident": document["ident"]})
                r = RGBValues["r"]
                r = convertToBinary(r)
                g = RGBValues["g"]
                g = convertToBinary(g)
                b = RGBValues["b"]
                b = convertToBinary(b)
                #Checking what state the light is in
                if ((r==0) and (g==0) and (b==0)):
                    userInput = "switchOff"
                elif ((r==0) and (g==0) and (b==1)):
                    userInput = "blue"
                elif ((r==0) and (g==1) and (b==0)):
                    userInput = "green"
                elif ((r==0) and (g==1) and (b==1)):
                    userInput = "cyan"
                elif ((r==1) and (g==0) and (b==0)):
                    userInput = "red"
                elif ((r==1) and (g==0) and (b==1)):
                    userInput = "purple"
                elif ((r==1) and (g==1) and (b==0)):
                    userInput = "yellow"
                elif ((r==1) and (g==1) and (b==1)):
                    userInput = "white"
                #Sending the server the id of the device
                serverMessageSend(document["ident"])
                #Sending the server what state the light should be on
                serverMessageSend(userInput)
        except TypeError:
            pass

#A function to determing what status the plug should be on
def plugCheck():
    #Creating a main loop in which to run
    while True:
        #Getting the information from the plug table
        plugsDict = devicesDB.plug.find({})
        try:
            #Getting the information for all the different plugs
            for document in plugsDict:
                #Getting the program to sleep for 1 second
                time.sleep(1)
                #Getting the ID and the state of the plug
                plugsData = devicesDB.plug.find_one({"ident": document["ident"]})
                state = plugsData["state"]
                #Checking the state of the plug and setting it to the current state
                if state:
                    userInput = "turnOn"
                elif not state:
                    userInput = "turnOff"
                #Sending a message to the server with the ID of the plug
                serverMessageSend(document["ident"])
                #Sending the state of the plug to the server
                serverMessageSend(userInput)
        except TypeError:
            pass

#Creating a main method in which to run the program
if __name__ == "__main__":
    #Printing to the console that the user program has started up
    print(getTime() + "User initiated")
    #Connecting to the server
    server = connectToServer()
    dbClient = pymongo.MongoClient("localhost", 27017)
    #Connecting to the mongodb server
    devicesDB = dbClient.weblightDatabase

    #Setting the client ID and sending it to the server
    clientID = "user"
    serverMessageSend(clientID)

    #Starting all the threads for the program
    lightThread = Thread(target=lightCheck)
    plugThread = Thread(target=plugCheck)
    lightThread.start()
    plugThread.start()
