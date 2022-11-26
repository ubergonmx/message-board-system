import socket
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
Message = "Hello, Server"
Input = ""
while Input != "leave":
    Input = input("Enter your command: ")
    if Input[:5] == "join ":
        print("join")
    elif Input[:9] == "register ":
        print("register")
    elif Input[:4] == "all ":
        print("all")
    elif Input[:4] == "msg ":
        print("message")
    elif Input == "?":
        print("Input syntax:")
        print("Description Input                        | Syntax Sample                 | Input Script\n")
        print("Connect to the server application        | /join <server_ip_add> <port>  | /join 192.168.1.1 12345")
        print("Disconnect to the server application     | /leave                        | /leave")
        print("Register a unique handle or alias        | /register <handle>            | /register Student1")
        print("Send message to all                      | /all <message>                | /all Hello World!")
        print("Send direct message to a single handle   | /msg <handle> <message>       | /msg Student1 Hello!")
        print("Help to output all Input Syntax commands | /?                            | /?\n")
    elif Input == "leave":
        break;
    else:
        print("Invalid Command")

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(str.encode(Message), (UDP_IP_ADDRESS, UDP_PORT_NO))