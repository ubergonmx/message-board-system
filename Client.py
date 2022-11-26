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
import json
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = "Hello, Server"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Input = ""
while Input != "leave":
    Input = input("Enter your command: ")
    json = {}
    if Input[:5] == "join ":    
        json = {'command': 'join'}
        print("join")
    elif Input == "leave":
        json = {'command': 'leave'}
        break;    
    elif Input[:9] == "register ":
        json = {'command': 'register', 'handle': 'handle'}       
        print("register")
    elif Input[:4] == "all ":
        json = {"command": "all", "message": Message}
        print(str.encode(str(json)))
        clientSock.sendto(str.encode(str(json)), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("all")
        break;
    elif Input[:4] == "msg ":
        json = {'command': 'msg', 'handle': 'handle',  'message': 'message'}
        print("message")
    elif Input == "?":
        syntaxcommands()
    else:
        json = {'command': 'all', 'message': '<error_message>'}
        print("Invalid Command")


