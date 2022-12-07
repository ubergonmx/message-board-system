## Again we import the necessary socket python module
import socket
import sys
import json

## Here we define the UDP IP address as well as the port number that we have
## already defined in the client python script.
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12345
## declare our serverSocket upon which
## we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## One difference is that we will have to bind our declared IP address
## and port number to our newly declared serverSock
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

registrants = {}
currentUsers = {}
addresses = []

while True:
    response = {}
    data, addr = serverSock.recvfrom(1024)    
    data = data.decode('utf-8')
    json_obj = json.loads(data)
    print (json_obj)
    
    if (json_obj['command'] == "join"):
        response = {"response": "Connection to the Message Board Server is successful!"}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
        addresses.append(addr)
    elif (json_obj['command'] == "leave"):
        response = {"response": "Connection closed. Thank you!"}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
        if (addr in registrants.values()):
            registrants.pop(currentUsers.get(addr))
        if (addr in currentUsers.keys()):    
            currentUsers.pop(addr)
        if (addr in addresses):
            addresses.remove(addr)
        if (len(addresses)==0):
            break;
    elif (json_obj['command'] == "register"):
        if (json_obj['handle'] not in registrants.keys()):
            msg = "Welcome, " + json_obj['handle']
            response = {"response": msg}
            registrants.update({json_obj['handle']: addr})
            currentUsers.update({addr: json_obj['handle']})
        else:
            response = {"response": "Error: Registration failed. Handle or alias already exists."}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))     
    elif (json_obj['command'] == "msg"):
        if (addr not in currentUsers.keys()):
            response = {"response": "Error: You need to be registered to send a message."}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (addr))
        elif (json_obj['handle'] not in registrants.keys()):
            response = {"response": "Error: Handle or alias not found."}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (addr))     
        elif (json_obj['handle'] not in currentUsers.values()):
            msg = "(To " + json_obj['handle'] + ") " + json_obj['message']
            response = {"response": msg}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (registrants.get(currentUsers.get(addr))))
        else:
            msg = "(To " + json_obj['handle'] + ") " + json_obj['message']
            response = {"response": msg}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (registrants.get(currentUsers.get(addr))))
            msg = "(From " + str(currentUsers.get(addr)) + ") " + json_obj['message']
            response = {"response": msg}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (registrants.get(json_obj['handle'])))
    elif (json_obj['command'] == "all"):
        if (addr not in currentUsers.keys()):
            response = {"response": "Error: You need to be registered to send a message."}
            response = json.dumps(response)
            serverSock.sendto(bytes(response, "utf-8"), (addr))
        else:
            msg = str(currentUsers.get(addr)) + ": " + json_obj['message']
            allUsers = list(currentUsers.keys())
            for userAddr in allUsers:
                response = {"response": msg}
                response = json.dumps(response)
                serverSock.sendto(bytes(response, "utf-8"), (userAddr))
    elif (json_obj['command'] == "error"):
        response = {"response": "Error: Command not found."}
        response = json.dumps(response)
        serverSock.sendto(bytes(response, "utf-8"), (addr))
    # stop server

    print(registrants)
    print(currentUsers)
    print(addresses)
