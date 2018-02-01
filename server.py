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

#Asking the user to set up the server by typing in the ip
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

#Getting the server to listen for a device to connect to it
server.listen(1)

#Defining the connected device and accepting the connection
receiver, address = server.accept()

#Printing a log of the date and time and the device that the server has connected to
print(getTime() + "Connected to " + str(address))

#Setting the value for the incoming message to None/Null
message = None

#Creating a main loop for the program to listen for incoming messages and respond accordingly
while True:
    #Assigning the variable message to the whatever message has been received
    message = receiver.recv(1024)
    #Decoding the message
    message = message.decode()
    
    #Determining what the message wants the server to do
    if message == "on":
        print(getTime() + "Light turned on")
    if message == "off":
        print(getTime() + "Light turned off")
