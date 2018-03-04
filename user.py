from generalFunctions import *
import pymongo


#A function to send the server a message
def serverMessageSend(message):
    server.send(message.encode())

def lightCheck():
    newMessage = ""
    message = ""


    #Creating a main loop in whcih the user can send messages to the server
    while True:
        lightsDict = devicesDB.lightBulb.find({})
        try:
            for document in lightsDict:
                time.sleep(1)
                RGBValues = devicesDB.lightBulb.find_one({"ident": document["ident"]})
                r = RGBValues["r"]
                g = RGBValues["g"]
                b = RGBValues["b"]
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
                serverMessageSend(document["ident"])
                serverMessageSend(userInput)
        except TypeError:
            pass

def plugCheck():
    while True:
        plugsDict = devicesDB.plug.find({})
        try:
            for document in plugsDict:
                time.sleep(1)
                plugsData = devicesDB.plug.find_one({"ident": document["ident"]})
                state = plugsData["state"]
                if state:
                    userInput = "turnOn"
                elif not state:
                    userInput = "turnOff"
                serverMessageSend(document["ident"])
                serverMessageSend(userInput)
        except TypeError:
            pass

#Creating a main method in which to run the program
if __name__ == "__main__":
    print(getTime() + "User initiated")
    server = connectToServer()
    dbClient = pymongo.MongoClient("localhost", 27017)
    devicesDB = dbClient.weblightDatabase

    #Setting the client ID and sending it to the server
    clientID = "user"
    serverMessageSend(clientID)

    lightThread = Thread(target=lightCheck)
    plugThread = Thread(target=plugCheck)
    lightThread.start()
    plugThread.start()
