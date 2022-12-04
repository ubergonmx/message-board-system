def syntaxcommands():
    print("Input syntax:")
    print("Description Input                        | Syntax Sample                 | Input Script\n")
    print("Connect to the server application        | /join <server_ip_add> <port>  | /join 192.168.1.1 12345")
    print("Disconnect to the server application     | /leave                        | /leave")
    print("Register a unique handle or alias        | /register <handle>            | /register Student1")
    print("Send message to all                      | /all <message>                | /all Hello World!")
    print("Send direct message to a single handle   | /msg <handle> <message>       | /msg Student1 Hello!")
    print("Help to output all Input Syntax commands | /?                            | /?\n")

def outputbox():
    while True:
        data, server = clientSock.recvfrom(1024)  
        data = data.decode('utf-8')
        #data = data.replace("'", '"')
        data = json.loads(data)
        print("\n------------FROM SERVER-------------")
        print (data['response'])
        print("------------FROM SERVER-------------\n")
        if stop_threads:
            break


import socket
import sys
import json
import threading

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Input = ""
allowed = 0;
outputbox = threading.Thread(target=outputbox)
while allowed == 0:
    Input = input()
    json_obj = {}
    
    if Input[:5] == "join ":        
        string = Input.split()   
        json_obj = {'command': 'join'}
        json_obj = json.dumps(json_obj)
        if (string[1] == "127.0.0.1" and string[2] == "6789"):
            allowed = 1 
            clientSock.sendto(bytes(json_obj, "utf-8"), ("127.0.0.1", 6789))
        else:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
    elif Input == "leave":
        json_obj = {'command': 'leave'}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        break;  
    elif Input == "?":
        syntaxcommands()
    else:
        print ('Command not found.')
        
stop_threads = False    
if allowed == 1:
    outputbox.start()  
        
while allowed == 1:
    Input = input()
    json_obj = {}
    if Input[:9] == "register ":
        string = Input.split()  
        json_obj = {'command': 'register', 'handle': str(string[1])}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
    elif Input == "leave":
        json_obj = {'command': 'leave'}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        allowed = 0; 
    elif Input[:4] == "msg ":
        string = Input.split(' ', 2) 
        json_obj = {'command': 'msg', 'handle': string[1],  'message': string[2]}  
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
    elif Input[:4] == "all ":
        string = Input.split(' ', 1) 
        json_obj = {"command": "all", "message": string[1]}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        print("all")
    elif Input == "?":
        syntaxcommands()
    else:
        json_obj = {'command': 'error', 'message': '<error_message>'}
        json_obj = json.dumps(json_obj)
        clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        
stop_threads = True   
outputbox.join()
