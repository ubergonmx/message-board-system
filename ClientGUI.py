import customtkinter
from tkinter import messagebox
import socket
import sys
import json
import threading


def outputbox():
    while True:
        try:
            data, server = clientSock.recvfrom(1024)  
            data = data.decode('utf-8')
            data = json.loads(data)
            app.insert_text(data['response'], "server")
            print("\n------------FROM SERVER-------------")
            print (data['response'])
            print("------------FROM SERVER-------------\n")
            if stop_threads:
                break
        except:
            app.insert_text("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", "error")
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")



Input = ""
allowed = 0
stop_threads = False
outputbox = threading.Thread(target=outputbox)
outputbox.daemon = True
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
json_obj = {}

class App(customtkinter.CTk):

    defaultTitle = "Message Board System - Client GUI "
    leave = False

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
        self.title(self.defaultTitle)
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
        self.textbox.tag_config("server", background="#17A2B8")
        self.textbox.tag_config("help1", background="#FFC107", foreground="#343A40")
        self.textbox.tag_config("help2", foreground="#FFC107")
        self.textbox.tag_config("error", background="#DC3545")
        # self.textbox.tag_config("private", background="#343A40")
        self.textbox.configure(state="disabled")

        self.combobox = customtkinter.CTkComboBox(master=self, values=self.syntaxPresets)
        self.combobox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, command=self.send_callback, text="Send command")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    def change_title(self, title):
        self.title(title)

    def insert_text(self, text, config=""):
        self.textbox.configure(state="normal")
        if config == "server":
            self.textbox.insert("insert", text + "\n", "server")
        elif config == "help1":
            self.textbox.insert("insert", text + "\n", "help1")
        elif config == "help2":
            self.textbox.insert("insert", text + "\n", "help2")
        elif config == "error":
            self.textbox.insert("insert", text + "\n", "error")
        else:
            self.textbox.insert("insert", text + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def send_callback(self):
        if self.combobox.get() != "" and not str.isspace(self.combobox.get()):
            self.insert_text(self.combobox.get())
            self.check_input(self.combobox.get())
            if not self.leave:
                self.combobox.set("")
            else:
                print("Closing Client GUI...")
                self.destroy()
            

    def check_input(self, Input):
        global allowed, outputbox, clientSock
        if allowed == 0:
            if Input[:5] == "join ":        
                string = Input.split()   
                if (len(string) == 3):
                    json_obj = {'command': 'join'}
                    json_obj = json.dumps(json_obj)
                    # try:
                    if (string[1] == "127.0.0.1" and string[2] == "6789"):
                        allowed = 1
                        clientSock.sendto(bytes(json_obj, "utf-8"), ("127.0.0.1", 6789))
                        outputbox.start()
                    else:
                        self.insert_text("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", "error")
                    # except:
                    #     self.insert_text("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", "error")
                else:
                    self.insert_text("Error: Command parameters do not match or is not allowed.", "error")
            elif Input == "leave":
                self.insert_text("Error: Disconnection failed. Please connect to the server first.", "error")
            elif Input == "?":
                i = 0
                for text in self.syntaxHelp:
                    if (i == 0):
                        self.insert_text(text, "help1")
                    else:
                        self.insert_text(text, "help2")
                    i += 1
            else:
                self.insert_text('Command not found or not allowed until user joins the server.', "error")
        elif allowed == 1:
            if Input[:9] == "register ":
                string = Input.split(' ', 1) 
                if (len(string) == 2):
                    json_obj = {'command': 'register', 'handle': string[1]}
                    json_obj = json.dumps(json_obj)
                    clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
                    self.change_title(self.defaultTitle + "(" + string[1] + ")")
                else:
                    self.insert_text("Error: Command parameters do not match or is not allowed.", "error")
            elif Input == "leave":
                json_obj = {'command': 'leave'}
                json_obj = json.dumps(json_obj)
                clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
                self.change_title(self.defaultTitle)
                self.leave = True
            elif Input[:4] == "msg ":
                string = Input.split(' ', 2) 
                if (len(string) == 3):
                    json_obj = {'command': 'msg', 'handle': string[1],  'message': string[2]}  
                    json_obj = json.dumps(json_obj)
                    clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
                else:
                    self.insert_text("Error: Command parameters do not match or is not allowed.", "error")
            elif Input[:4] == "all ":
                string = Input.split(' ', 1) 
                if (len(string) == 2):
                    json_obj = {"command": "all", "message": string[1]}
                    json_obj = json.dumps(json_obj)
                    clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
                else:
                    self.insert_text("Error: Command parameters do not match or is not allowed.", "error")
            elif Input == "?":
                i = 0
                for text in self.syntaxHelp:
                    if (i == 0):
                        self.insert_text(text, "help1")
                    else:
                        self.insert_text(text, "help2")
                    i += 1
            else:
                json_obj = {'command': 'error', 'message': '<error_message>'}
                json_obj = json.dumps(json_obj)
                clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))

def on_closing():
    global allowed, clientSock
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if allowed == 1:
            json_obj = {'command': 'leave'}
            json_obj = json.dumps(json_obj)
            clientSock.sendto(bytes(json_obj, "utf-8"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        clientSock.close()
        app.destroy()

app = App()
if __name__ == "__main__":
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
    raise SystemExit