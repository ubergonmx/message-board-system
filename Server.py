## Again we import the necessary socket python module
import socket
import sys
import json

## Here we define the UDP IP address as well as the port number that we have
## already defined in the client python script.
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
## declare our serverSocket upon which
## we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## One difference is that we will have to bind our declared IP address
## and port number to our newly declared serverSock
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

registrants = []

while True:
    response = {}
    data, addr = serverSock.recvfrom(1024)    
    data = data.decode('utf-8')
    data = data.replace("'", '"')
    print ("Message: ", data)
    json_obj = json.loads(data)
    print (json_obj['command'])
    
    if (json_obj['command'] == "join"):
        response = {"response": "Connection to the Message Board Server is successful!"}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
    elif (json_obj['command'] == "leave"):
        response = {"response": "Connection closed. Thank you!"}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
        break;
    elif (json_obj['command'] == "register"):
        if (json_obj['handle'] not in registrants):
            msg = "Welcome, " + json_obj['handle']
            response = {"response": msg}
            registrants.append(json_obj['handle'])
        else:
            response = {"response": "Error: Registration failed. Handle or alias already exists."}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
        print(registrants)
    elif (json_obj['command'] == "error"):
        response = {"response": "Error: Command not found."}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
    
