import customtkinter
import socket
import sys
import json


# def outputbox():
#     while True:
#         data, server = clientSock.recvfrom(1024)  
#         data = data.decode('utf-8')
#         data = json.loads(data)
#         print("\n------------FROM SERVER-------------")
#         print (data['response'])
#         print("------------FROM SERVER-------------\n")
#         if stop_threads:
#             break



# Input = ""
# allowed = 0
# outputbox = threading.Thread(target=outputbox)
# while allowed == 0:
#     Input = input()
#     json_obj = {}
    
#     if Input[:5] == "join ":        
#         string = Input.split()   
#         if (len(string) == 3):
#             json_obj = {'command': 'join'}
#             json_obj = json.dumps(json_obj)
#             if (string[1] == "127.0.0.1" and string[2] == "6789"):
#                 allowed = 1 
#                 clientSock.sendto(bytes(json_obj, "utf-8"), ("127.0.0.1", 6789))
#             else:
#                 print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
#         else:
#             print("Error: Command parameters do not match or is not allowed.")
#     elif Input == "leave":
#         print("Error: Disconnection failed. Please connect to the server first.")
#     elif Input == "?":
#         syntaxcommands()
#     else:
#         print ('Command not found or not allowed until user joins the server.')
        
# stop_threads = False    
# if allowed == 1:
#     outputbox.start()  
        
# while allowed == 1:
#     Input = input()
#     json_obj = {}
#     if Input[:9] == "register ":
#         string = Input.split(" ", 1)  
#         if (len(string) == 2):
#             json_obj = {'command': 'register', 'handle': str(string[1])}
#             json_obj = json.dumps(json_obj)
#             clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
#         else:
#             print("Error: Command parameters do not match or is not allowed.")
#     elif Input == "leave":
#         json_obj = {'command': 'leave'}
#         json_obj = json.dumps(json_obj)
#         clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
#         allowed = 0; 
#     elif Input[:4] == "msg ":
#         string = Input.split(' ', 2) 
#         if (len(string) == 3):
#             json_obj = {'command': 'msg', 'handle': string[1],  'message': string[2]}  
#             json_obj = json.dumps(json_obj)
#             clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
#         else:
#             print("Error: Command parameters do not match or is not allowed.")
#     elif Input[:4] == "all ":
#         string = Input.split(' ', 1) 
#         if (len(string) == 2):
#             json_obj = {"command": "all", "message": string[1]}
#             json_obj = json.dumps(json_obj)
#             clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
#         else:
#             print("Error: Command parameters do not match or is not allowed.")
#     elif Input == "?":
#         syntaxcommands()
#     else:
#         json_obj = {'command': 'error', 'message': '<error_message>'}
#         json_obj = json.dumps(json_obj)
#         clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        
# stop_threads = True   
# outputbox.join()

class App(customtkinter.CTk):

    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 6789
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    syntaxHelp = [
        "Description Input\t\t\t\t\t| Syntax Sample\t\t\t| Input Script",
        "Connect to the server application\t\t\t\t\t| join <server_ip_add> <port>\t\t\t| join " + UDP_IP_ADDRESS + " " + str(UDP_PORT_NO),
        "Disconnect to the server application\t\t\t\t\t| leave\t\t\t| leave",
        "Register a unique handle or alias\t\t\t\t\t| register <handle>\t\t\t| register Student1",
        "Send message to all\t\t\t\t\t| all <message>\t\t\t| all Hello World!",
        "Send direct message to a single handle\t\t\t\t\t| msg <handle> <message>\t\t\t| msg Student1 Hello!",
        "Help to output all Input Syntax commands\t\t\t\t\t| ?\t\t\t| ?\n"
    ]
    
    syntaxPresets = [
        "join " + UDP_IP_ADDRESS + " " + str(UDP_PORT_NO), 
        "leave",
        "register <handle>",
        "all <message>",
        "msg <handle> <message>",
        "?"
    ]

    def __init__(self):
        super().__init__()

        self.geometry("700x300")
        self.title("Message Board System - Client GUI")
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="disabled")

        self.combobox = customtkinter.CTkComboBox(master=self, values=self.syntaxPresets)
        self.combobox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, command=self.send_callback, text="Send command")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    def insert_text(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("insert", text + "\n")
        self.textbox.configure(state="disabled")

    def send_callback(self):
        self.insert_text(self.combobox.get())
        self.checkInput(self.combobox.get())

    def checkInput(self, Input):
        json_obj = {}
    
        if Input[:5] == "join ":        
            string = Input.split()   
            if (len(string) == 3):
                json_obj = {'command': 'join'}
                json_obj = json.dumps(json_obj)
                if (string[1] == "127.0.0.1" and string[2] == "6789"):
                    allowed = 1 
                    self.clientSock.sendto(bytes(json_obj, "utf-8"), ("127.0.0.1", 6789))
                    self.insert_text("Connected to server.")
                else:
                    self.insert_text("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            else:
                self.insert_text("Error: Command parameters do not match or is not allowed.")
        elif Input == "leave":
            self.insert_text("Error: Disconnection failed. Please connect to the server first.")
        elif Input == "?":
            for i in self.syntaxHelp:
                self.insert_text(i)
        else:
            self.insert_text('Command not found or not allowed until user joins the server.')

if __name__ == "__main__":
    app = App()
    app.mainloop()