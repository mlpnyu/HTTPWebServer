# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.bind(("10.0.0.138", port))
    serverSocket.listen(1)
    #print("HTTP server started...")
    while True:
        connectionSocket, addr = serverSocket.accept()
        try:
            try:
                message = connectionSocket.recv(1024).decode()
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read()
                #print(outputdata)
                # Send one HTTP header line into socket.
                #print("Sending header")
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                # Send the content of the requested file to the client
                #print("Sending file")
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                #print("File not found")
                connectionSocket.send("HTTP/1.1 404 File not found\r\n".encode())
                connectionSocket.close()
        except (ConnectionResetError, BrokenPipeError):
            #print("connection or pipe error")
            pass
        serverSocket.close()
        sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)