#Imports the TCP socket package
import socket
#Imports a package to get the current date and time for timestamping
import datetime

#Creating a function to get the current date and time and formatting it
def getTime():
    #Converting the current date and time to a string
    currentTime = str(datetime.datetime.now())
    #Selecting only the information that we want to display
    currentTime = (currentTime[0:19] + ": ")
    #Returning the current date and time
    return currentTime

#Asking the user to set up the server by typing in the ip. (USE "localhost" if you are running both programs on the same computer)
print("Input the server ip")
#Getting the user input for the ip
ip = input()

#Asking the user to input a port for the server
print("Input the port")
#Getting the user input for the port and then coverting it to an integer
port = int(input())

#Creatign a socket for the client to connect to the server
client = socket.socket()

#Trying to connect to the server using the ip and port specified by the user
client.connect((ip,port))

#Once successfully connected it prints a log of the date and time and the ip it has connected to
print(getTime() + "Connected to " + ip)

#Tells the user what they can do
print("Type on or off to switch the light on or off")

#Creating a main loop in which the user can send messages to the server
while True:
    #Resetting the value for the message
    message = ""
    
    #Getting the user input
    switch = input()
    
    #Determining what the user wants to do and sending the appropriate message to the server
    if switch == "on":
        message = "on"
        #Encoding the message and then sending it to the server
        client.send(message.encode())
        #Printing a log of the date and time and the action performed
        print(getTime() + "Light turned on")
   
    elif switch == "off":
        message = "off"
        #Encoding the message and then sending it to the server
        client.send(message.encode())
        #Printing a log of the date and time and the action performed
        print(getTime() + "Light turned off")
   
    else:
        print("That was not a valid input")
