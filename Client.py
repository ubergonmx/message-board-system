def syntaxcommands():
    print("Input syntax:")
    print("Description Input                        | Syntax Sample                 | Input Script\n")
    print("Connect to the server application        | /join <server_ip_add> <port>  | /join 192.168.1.1 12345")
    print("Disconnect to the server application     | /leave                        | /leave")
    print("Register a unique handle or alias        | /register <handle>            | /register Student1")
    print("Send message to all                      | /all <message>                | /all Hello World!")
    print("Send direct message to a single handle   | /msg <handle> <message>       | /msg Student1 Hello!")
    print("Help to output all Input Syntax commands | /?                            | /?\n")


import socket
import sys
import json
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = "Hello, Server"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Input = ""
allowed = 0;

while True:
    Input = input("Enter your command: ")
    json_obj = {}
    
    if Input[:5] == "join ":        
        string = Input.split()   
        json_obj = {'command': 'join'}
        json_obj = json.dumps(json_obj)
        if (string[1] == "127.0.0.1" and int(string[2]) == 6789):
            allowed = 1 
            clientSock.sendto(bytes(json_obj, "utf-8"), ("127.0.0.1", 6789))
        else:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
    elif Input == "leave":
        json_obj = {'command': 'leave'}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        break;    
    elif Input[:9] == "register ":
        string = Input.split()  
        json_obj = {'command': 'register', 'handle': str(string[1])}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
    elif Input[:4] == "all ":
        json_obj = {"command": "all", "message": Message}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("all")
    elif Input[:4] == "msg ":
        json_obj = {'command': 'msg', 'handle': 'handle',  'message': 'message'}
        print("message")
    elif Input == "?":
        syntaxcommands()
    else:
        json_obj = {'command': 'error', 'message': '<error_message>'}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        
    if (allowed == 1):
        data, server = clientSock.recvfrom(1024)  
        if data:
            data = data.decode('utf-8')
            data = data.replace("'", '"')
            data = json.loads(data)
            print (data)
        
